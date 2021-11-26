import json
from typing import Any, Callable, Dict, List, Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse


class ProcessAction:
    data: Dict[str, Any] = {}
    actions: Dict[str, Optional[List[Callable]]] = {}
    checks: Dict[str, Optional[List[Callable]]] = {}

    _request: WSGIRequest
    _response: Dict[str, Any]

    # =========================================================================

    def add_checks(self, name: str, *checks: Callable) -> "ProcessAction":
        if name in self.checks:
            self.checks[name] += list(checks)  # type: ignore
        else:
            self.checks[name] = list(checks)

        return self

    # =========================================================================

    def add_actions(self, name: str, *functions: Callable) -> "ProcessAction":
        if name in self.actions:
            self.actions[name] += list(functions)  # type: ignore
        else:
            self.actions[name] = list(functions)

        return self

    # =========================================================================

    def process(self, request: WSGIRequest, **extra_values):
        self._request = request
        self.data = json.loads(request.body.decode())

        if extra_values:
            self.data["values"] |= extra_values

        if (act := self.data.get("action")) not in self.actions:
            self._response = {
                "data": {
                    "success": False,
                    "message": "Unknown action.",
                },
                "status": 400,
            }

        for check in self.checks[act]:  # type: ignore
            if res := check(self._request, self.data):
                if res[0]:
                    self.data["values"] |= res[1]
                else:
                    self._response = res[1]

        actions_output = []
        for action in self.actions[act]:  # type: ignore
            if res := action(self._request, self.data):
                if not res[0]:
                    self._response = {
                        "data": {
                            "success": False,
                            "message": "Unknown error.",
                        },
                        "status": 500,
                    }
                else:
                    actions_output.append(res[1])

        self._response = {
            "data": {"success": True, "message": actions_output},
            "status": 200,
        }

    # =========================================================================

    def response(self) -> JsonResponse:
        return JsonResponse(**self._response)
