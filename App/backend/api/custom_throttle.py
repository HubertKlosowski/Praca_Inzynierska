from rest_framework import throttling


class MakeSubmissionUserRateThrottle(throttling.UserRateThrottle):
    scope = 'make_submission_user'
    rate = '100/day'  # '100/day'

class MakeSubmissionAnonRateThrottle(throttling.AnonRateThrottle):
    scope = 'make_submission_anon'
    rate = '1/day'  # '1/day'

class LoginRateThrottle(throttling.UserRateThrottle):
    scope = 'login_user'
    rate = '5/hour'  # '5/hour'

class CreateUserRateThrottle(throttling.AnonRateThrottle):
    scope = 'create_user'
    rate = '1/day'  # 1/day

class UpdateUserRateThrottle(throttling.UserRateThrottle):
    scope = 'update_user'
    rate = '1/day'  # '1/day'

class DeleteUserRateThrottle(throttling.UserRateThrottle):
    scope = 'delete_user'
    rate = '1/day'  # '1/day'

class RenewSubmissionUserRateThrottle(throttling.UserRateThrottle):
    scope = 'renew_submission_user'
    rate = '1/day'  # '1/day'