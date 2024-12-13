from django.contrib import messages


class Message:
    def __init__(self, request):
        self.request = request

    def success(self, message):
        messages.success(self.request, message)

    def warning(self, message):
        messages.warning(self.request, message)

    def error(self, message):
        messages.error(self.request, message)

    def info(self, message):
        messages.info(self.request, message)
