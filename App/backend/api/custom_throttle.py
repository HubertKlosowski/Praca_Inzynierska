from rest_framework import throttling


class MakeSubmissionUserRateThrottle(throttling.UserRateThrottle):
    scope = 'make_submission_user'
    rate = '100/day'  # 100/day

class MakeSubmissionAnonRateThrottle(throttling.AnonRateThrottle):
    scope = 'make_submission_anon'
    rate = '1/day'  # 1/day

class LoginRateThrottle(throttling.UserRateThrottle):
    scope = 'login_user'
    rate = '5/hour'  # 5/hour

class CreateUserRateThrottle(throttling.AnonRateThrottle):
    scope = 'create_user'
    rate = '1/day'  # 1/day

class UpdateUserRateThrottle(throttling.UserRateThrottle):
    scope = 'update_user'
    rate = '1/day'  # 1/day

class DeleteUserRateThrottle(throttling.UserRateThrottle):
    scope = 'delete_user'
    rate = '1/day'  # 1/day

class VerifyUserUserRateThrottle(throttling.UserRateThrottle):
    scope = 'admin_panel'
    rate = '10/day'  # 10/day

class RenewSubUserRateThrottle(throttling.UserRateThrottle):
    scope = 'renew_sub_user'
    rate = '10/day'  # 10/day

class ChangeSubNameUserRateThrottle(throttling.UserRateThrottle):
    scope = 'change_sub_name_user'
    rate = '50/day'  # 50/day

class GetSubUserRateThrottle(throttling.UserRateThrottle):
    scope = 'get_sub_user'
    rate = '50/day'  # 50/day


def allow_request_for_test():
    def _allow_request(self, request, view):
        return True

    CreateUserRateThrottle.allow_request = _allow_request
    DeleteUserRateThrottle.allow_request = _allow_request
    UpdateUserRateThrottle.allow_request = _allow_request