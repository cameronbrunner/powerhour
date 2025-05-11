import os
from flask import Flask, request

from synochat.webhooks import SlashCommand, OutgoingWebhook
from synochat.exceptions import *
import lib3relind

app = Flask(__name__)

class PowerController:
    def __init__(self, device, relay):
        self.device = device
        self.relay = relay

    def get_status(self):
        if lib3relind.get(self.device,self.relay) == 1:
            return 'The power is on!'
        return 'The power is off!'

    def set_power(self, state):
        lib3relind.set(self.device,self.relay,state)

    def process_command(self, command, *args):
        print('Processing command [%s]' % command, flush=True)
        match command:
            case 'status':
                pass
            case 'on':
                self.set_power(1)
            case 'off':
                self.set_power(0)
            case _:
                raise Exception('Invalid command specified [%s].  Must be "status", "off", or "on".' % command)
        return self.get_status()

pc = PowerController(os.environ.get("DEVICE",0), os.environ.get("RELAY",2))

@app.route('/power', methods=['POST'])
def power():
    token = os.environ.get("WEBHOOK_TOKEN")
    webhook = OutgoingWebhook(request.form, token, verbose=True)

    if not webhook.authenticate(token):
        return webhook.createResponse('Outgoing Webhook authentication failed: Token mismatch.')

    response = ''
    parts = webhook.text.split(' ')
    #print(parts, flush=True)
    if len(parts) == 2:
        try:
            response = pc.process_command(parts[1])
        except:
            # Couldn't parts the command so ignore...
            pass
    return webhook.createResponse(response)

@app.route('/slash', methods=['POST'])
def slash():
    token   = os.environ.get("SLASH_TOKEN")
    command = SlashCommand(request.form)

    if not command.authenticate(token):
        return command.createResponse('Invalid token.')

    # Check if the command parameters are valid
    try:
        action  = command.addParameter('action')
    except ParameterParseError:
        return command.createResponse('An action of "status" or "set" must be specified')

    try:
        return command.createResponse(pc.process_command(action.value))
    except Exception as ex:
        return command.createResponse('Error processing command: %s' % ex)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug = False)
