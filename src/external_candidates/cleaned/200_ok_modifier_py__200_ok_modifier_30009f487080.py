# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_200_ok_modifier.py\_200_ok_modifier_30009f487080.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\200-OK-Modifier\200_OK_modifier.py

# -*- coding: utf-8 -*-

from burp import IBurpExtender, IContextMenuFactory, IHttpListener

from java.util import ArrayList, List

from javax.swing import JCheckBoxMenuItem


class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks

        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("200 OK Modifier")

        callbacks.registerContextMenuFactory(self)

        callbacks.registerHttpListener(self)

        self.enabled = False

    def createMenuItems(self, invocation):
        self.context = invocation

        menu = ArrayList()

        activateMenuItem = JCheckBoxMenuItem("Change Response to 200 OK", actionPerformed=self.toggleEnabled)

        deactivateMenuItem = JCheckBoxMenuItem("Disable response modifier", actionPerformed=self.toggleDisabled)

        if self.enabled:
            activateMenuItem.setSelected(True)

        else:
            deactivateMenuItem.setSelected(True)

        menu.add(activateMenuItem)

        menu.add(deactivateMenuItem)

        return menu

    def toggleEnabled(self, event):
        self.enabled = True

        self._callbacks.printOutput("200 OK Modifier enabled")

    def toggleDisabled(self, event):
        self.enabled = False

        self._callbacks.printOutput("200 OK Modifier disabled")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if self.enabled and not messageIsRequest:
            responseBytes = messageInfo.getResponse()

            responseInfo = self._helpers.analyzeResponse(responseBytes)

            if responseInfo.getStatusCode() != 200:
                headers = list(responseInfo.getHeaders())

                statusCode = responseInfo.getStatusCode()

                headers[0] = "HTTP/2 200 OK OriginalCodeWas: {}".format(statusCode)

                responseBody = responseBytes[responseInfo.getBodyOffset() :]

                newResponse = self._helpers.buildHttpMessage(headers, responseBody)

                messageInfo.setResponse(newResponse)
