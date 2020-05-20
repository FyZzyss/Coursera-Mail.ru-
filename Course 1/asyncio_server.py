import asyncio
import traceback


class CommonStorage:

    def __init__(self):
        self.data = {}

    def put(self, metrika, value, timestamp):
        if metrika not in self.data:
            self.data[metrika] = {}
        self.data[metrika][timestamp] = value
        return 'ok'

    def get(self, metrika):
        try:
            if metrika != '*':
                data = {
                    metrika: self.data.get(metrika, {})
                }
            else:
                data = self.data
            result = {}
            try:
                for metrika, timestamp_data in data.items():
                    result[metrika] = sorted(timestamp_data.items())
            except AttributeError:
                pass
            return result
        except:
            print(traceback.print_exc())


class Parser:
    def encode(self, responses):
        try:
            answers = []
            for response in responses:
                if response == 'ok':
                    return 'ok\n\n'
                else:
                    for metrika, values in response.items():
                        for timestamp, value in values:
                            answers.append(f'{metrika} {value} {timestamp}')
            result = 'ok\n'
            if answers:
                result += '\n'.join(answers) + '\n'
            return result + '\n'
        except:
            # print(traceback.print_exc())
            pass

    def decode(self, data):
        print(data)
        parts = data.split('\n')
        commands = []
        for part in parts:
            if not part:
                continue
            try:
                method, params = part.strip().split(" ", 1)
                if (len(params.strip().split(" ")) != 1 and method == 'get') or (
                        len(params.strip().split(" ")) != 3 and method == 'put'):
                    raise ValueError("wrong command")
                if method == 'put':
                    metrika, value, timestamp = params.split()
                    commands.append(
                        (method, metrika, float(value), int(timestamp))
                    )
                elif method == 'get':
                    metrika = params
                    commands.append(
                        (method, metrika)
                    )
                else:
                    # print(traceback.print_exc())
                    raise ValueError("wrong command")
            except ValueError:
                # print(traceback.print_exc())
                raise ValueError("wrong command")

        return commands


class Builder:
    def __init__(self, storage):
        self.storage = storage

    def run(self, method, *params):
        if method == 'put':
            # print('RUN PUT WITH PARAMS:', params)
            return self.storage.put(*params)
        elif method == 'get':
            # print('RUN GET WITH PARAMS:', params)
            return self.storage.get(*params)


class ClientProtocol(asyncio.Protocol):
    storage = CommonStorage()

    def __init__(self):
        super().__init__()
        self.parser = Parser()
        self.builder = Builder(self.storage)
        self._asyncBuffer = b''

    def work_with_data(self, data):
        commands = self.parser.decode(data)
        messages = []
        for command in commands:
            resp = self.builder.run(*command)
            messages.append(resp)
        return self.parser.encode(messages)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self._asyncBuffer = data
        try:
            decoded_data = self._asyncBuffer.decode()
        except UnicodeDecodeError:
            self.transport.write(f'error\nwrong command\n\n'.encode())
            return
        if not decoded_data.endswith('\n') or decoded_data == '\n':
            self.transport.write(f'error\nwrong command\n\n'.encode())
            return
        try:
            resp = self.work_with_data(decoded_data)
        except (ValueError, Exception) as err:
            self.transport.write(f'error\n{err}\n\n'.encode())
            return
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    # запуск сервера для тестирования
    run_server('127.0.0.1', 8888)
