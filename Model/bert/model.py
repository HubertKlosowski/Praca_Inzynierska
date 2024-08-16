import torch
import torch.nn as nn


torch.manual_seed(1)


def positional_encoding(data: torch.Tensor, d_model: int, num_tokens: int, n: int) -> torch.Tensor:  # nie dla BERT
    pos_encoding = torch.zeros(size=(num_tokens, d_model), dtype=torch.float)
    for k in range(num_tokens):
        zeros = torch.zeros(size=(d_model, ), dtype=torch.float)
        i = torch.tensor([_ for _ in range(d_model // 2)], dtype=torch.float)
        arg = k / n ** (2 * i / d_model)
        zeros[:len(zeros) - 1:2] = torch.sin(arg)  # jeśli d_model jest nieparzysty
        zeros[1::2] = torch.cos(arg)
        pos_encoding[k] = zeros
    return pos_encoding + data


# Kodowanie słów różni się od podstawowego transformatora z 2017. Mamy 3 warstwy:
# 1. Reprezentacja tokenów przy wykorzystaniu ich ID w całym zbiorze tokenów
# 2. Reprezentacja pozycji poszczególnych tokenów w sekwencji
# 3. Reprezentacja typu tokena: czy należy do zdania A czy B (next sentence prediction)
# Na końcu wszystkie wygenerowane wektory są dodawane (standardowe operacje z normalizacją i dropoutem)
class BERTEmbedding(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, seq_length: int, device: str) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.seq_length = seq_length
        self.d_model = d_model
        self.device = device
        self.word_embeddings = nn.Embedding(vocab_size, d_model).to(device=self.device)
        self.positional_embeddings = nn.Embedding(seq_length, d_model).to(device=self.device)
        self.token_type_embeddings = nn.Embedding(2, d_model).to(device=self.device)
        self.layer_norm = LayerNorm(d_model, 1e-12)
        self.dropout = nn.Dropout(p=0.1)

    def forward(self, input_ids: torch.Tensor, token_type_ids: torch.Tensor) -> torch.Tensor:
        position_ids = torch.arange(self.seq_length).to(device=self.device)

        word_embeddings = self.word_embeddings(input_ids)
        positional_embeddings = self.positional_embeddings(position_ids)
        token_type_embeddings = self.token_type_embeddings(token_type_ids)

        final_embeddings = word_embeddings + positional_embeddings + token_type_embeddings
        after_norm = self.layer_norm(final_embeddings)
        after_dropout = self.dropout(after_norm)
        return after_dropout


class SingleHeadAttention(nn.Module):
    def __init__(self, d_k: int, device: str, mask: bool = False) -> None:
        super().__init__()
        self.d_k = d_k
        self.mask = mask

        self.device = device

    # Parametry wejściowe to Q, K, V.
    # Mnożymy macierz Q przez transponowaną macierz K. Skalujemy otrzymane wartości przez pierwiastek z d_model.
    # Aby wyłączyć niektóre słowa w obliczaniu ich 'attention score' można wykonać operację mask (wstawienie -inf).
    # Otrzymujemy oceny jak dane słowo wpływa na pozostałe dzięki zastosowaniu funkcji softmax. Jeśli maskowanie zostało
    # wybrane wartości -inf dają wartości 0.
    # Zwracamy macierz, która przechowuje znaczenie każdego słowa oraz relacje słów między sobą.
    # Wymiary (num_tokens x d_model)
    def forward(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        dot_product = torch.matmul(query, key.transpose(0, 1)) / (self.d_k ** 0.5)
        if self.mask:
            dot_product += torch.triu(torch.full(dot_product.shape, -torch.inf, device=self.device), diagonal=1)
        attention_weights = torch.softmax(dot_product, dim=-1)
        attention = torch.matmul(attention_weights, value)
        return attention


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, h: int, device: str) -> None:
        super().__init__()
        self.h = h  # ilość 'head'
        self.d_model = d_model
        self.Wq = nn.Linear(d_model, d_model).to(device=device)
        self.Wk = nn.Linear(d_model, d_model).to(device=device)
        self.Wv = nn.Linear(d_model, d_model).to(device=device)
        self.Wo = nn.Linear(d_model, d_model).to(device=device)
        self.heads = nn.ModuleList([SingleHeadAttention(d_model // self.h, device) for _ in range(self.h)])

    def forward(self, encoder_input: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        xd = attention_mask
        batch_dim = (encoder_input.shape[0], encoder_input.shape[1], self.h, encoder_input.shape[2] // self.h)
        query = self.Wq(encoder_input).reshape(batch_dim).transpose(1, 2)
        key = self.Wk(encoder_input).reshape(batch_dim).transpose(1, 2)
        value = self.Wv(encoder_input).reshape(batch_dim).transpose(1, 2)

        multi_head_output = torch.zeros_like(encoder_input)
        for i in range(encoder_input.shape[0]):
            # podział Q, K, V na części dla każdej z głów
            concat_heads = [head(query[i][j], key[i][j], value[i][j]) for j, head in enumerate(self.heads)]
            multi_head_output[i] = self.Wo(torch.cat(concat_heads, dim=1))
        return multi_head_output


# Jest to sieć, która w warstwie ukrytej korzysta z warstwy liniowej i funkcji aktywacji ReLU
# Warstwa wyjściowa to tylko warstwa liniowa
class FeedForwardNetwork(nn.Module):
    def __init__(self, d_model: int, d_ff: int) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, encoder_input: torch.Tensor) -> torch.Tensor:
        ffn_output = self.layers(encoder_input)
        return ffn_output


# Normalizacja wyjść z FFN (Feed-Forward Network) i MHA (Multi-Head Attention)
class LayerNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.layer_norm = nn.LayerNorm(d_model, eps=self.eps)

    def forward(self, encoder_input: torch.Tensor) -> torch.Tensor:
        layer_norm_output = self.layer_norm(encoder_input)
        return layer_norm_output


# Jedna warstwa enkodera zawierająca wszystkie części wyżej wymienione.
class EncoderLayer(nn.Module):
    def __init__(self, d_model: int, d_ff: int, h: int, device: str) -> None:
        super().__init__()
        self.multi_head = MultiHeadAttention(d_model, h=h, device=device)
        self.ffn = FeedForwardNetwork(d_model, d_ff)
        self.layer_norm = LayerNorm(d_model)

    def forward(self, encoder_input: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        after_multi_head = self.layer_norm(encoder_input + self.multi_head(encoder_input, attention_mask))
        after_ffn = self.layer_norm(after_multi_head + self.ffn(after_multi_head))
        return after_ffn


class Encoder(nn.Module):
    def __init__(self, d_model: int, d_ff: int, h: int, num_layers: int, device: str) -> None:
        super().__init__()
        self.layers = nn.ModuleList([EncoderLayer(d_model, d_ff, h, device) for _ in range(num_layers)])

    def forward(self, encoder_input: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        x = encoder_input
        for layer in self.layers:
            x = layer(x, attention_mask)
        return x


class BERT(nn.Module):
    def __init__(self, d_model: int, d_ff: int, h: int, num_layers: int, seq_length: int, device: str) -> None:
        super().__init__()
        self.bert_embedding = BERTEmbedding(30522, d_model, seq_length, device)
        self.encoder_part = Encoder(d_model=d_model, d_ff=d_ff, h=h, num_layers=num_layers, device=device)
        self.linear = nn.Linear(d_model, 2).to(device=device)

    def forward(self, input_ids: torch.Tensor, token_type_ids: torch.Tensor,
                attention_mask: torch.Tensor) -> torch.Tensor:
        word_embedding = self.bert_embedding(input_ids, token_type_ids)
        after_encoder = self.encoder_part(word_embedding, attention_mask)
        last_linear = self.linear(after_encoder)
        cls_output = last_linear[:, 0, :]  # interesują nas tylko wartosci z tokena [CLS]
        proba = torch.softmax(cls_output, dim=-1)
        return proba


# BERT BASE
#     num_layes = 12
#     d_ff = 3072
#     h = 12
#     embedd = 768

# BERT LARGE
#     num_layes = 24
#     d_ff = 4096
#     h = 16
#     embedd = 1024
