from flask import Flask, request

from synochat.webhooks import SlashCommand
from synochat.exceptions import *
import lib3relind

app = Flask(__name__)

def get_status(command, device, relay):
    if lib3relind.get(device,relay) == 1:
        return command.createResponse('The power is on!')
    return command.createResponse('The power is off!')

@app.route('/power', methods=['POST'])
def slash():
    token   = os.environ.get("SYN_TOKEN")
    device = os.environ.get("DEVICE",0)
    relay = os.environ.get("RELAY",2)
    command = SlashCommand(request.form)

    if not command.authenticate(token):
        return command.createResponse('Invalid token.')

    # Check if the command parameters are valid
    try:
        action  = command.addParameter('action')
        #state   = command.addParameter('state',  optional=True)
    except ParameterParseError:
        return command.createResponse('An action of "status" or "set" must be specified')

    try:
        match action.value:
            case 'status':
                pass
            case 'on':
                lib3relind.set(device,relay,1)
            case 'off':
                lib3relind.set(device,relay,0)
            case _:
                return command.createResponse('Invalid command specified [%s].  Must be "status", "off", or "on".' % action.value)
        return get_status(command, device, relay)
    except Exception as ex:
        return command.createResponse('Error processing command: %s' % ex)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug = True)
