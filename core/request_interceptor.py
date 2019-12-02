from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.request import Request
from rest_framework import exceptions
from django.db.models.query.sql import RawQuery
from .CustomLogger import CustomLogger


# TODO: This code isn't completed and not integrated

class HttpHeaderAuthentication(authentication.BaseAuthentication):
    log = CustomLogger.logger

    def do_auth(self, user_roles: [any]):
        # check database
        self.log.debug(f"checking if user roles [{user_roles}] has any privileges")

        prives: [any] = RawQuery.objects.raw(
            'select p.* from privileges p inner join roles r on p.role_id = r.role_id where r.role_name = %s',
            [user_roles])
        privileges = []
        for p in prives:
            privileges.append(p.priv_name)
        if len(privileges) == 0:
            # no roles available, this user shouldnt have come this far
            # user has no roles so we won't give any response
            self.log.debug(f"no privileges found for user roles [{user_roles}]")
            return []
        return privileges

    def authenticate(self, request: Request):
        self.log.debug(f"new request found, from {request.get_full_path()}")
        user_roles = request.headers.get('HTTP-USER-GROUPS-FIELD')
        privileges_from_db = self.do_auth(user_roles)
        print(f"found {len(privileges_from_db)} privileges for user_roles {user_roles}")

        u = User()
        u.Meta.groups = privileges_from_db
        # to set in response headers using myapi.request_control_middleware.AuthMiddleware class

        if len(privileges_from_db) == 0:
            print("no privileges found")
            raise exceptions.AuthenticationFailed('no privileges available')

        return u, None  # authentication successful
