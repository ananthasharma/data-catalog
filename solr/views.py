from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.CustomLogger import CustomLogger


class SolrPush(APIView):
    LOG = CustomLogger.logger

    def get(self, request: Request) -> Response:
        """No Need to build this just yet."""
        self.LOG.debug("Solr Push service invoked, this feature is not implemented yet")
        return Response(data=None, status=status.HTTP_501_NOT_IMPLEMENTED)
