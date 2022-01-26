import socket
import json


# To be able to use it you need the MQL5 Service to send the data, it is possible to found it here:
# -------------------------------------------------------------------- #
# Free:
#     https://www.mql5.com/en/market/product/57574
#   - Bollinger Bands
#   - MACD
#   - Moving Average
#   - OBV On Balance Volume
#   - Stochastic
#
# -------------------------------------------------------------------- #
#
# -------------------------------------------------------------------- #
# $30.00 Dollars per 3 month. ($10.00/month):
#     https://www.mql5.com/en/market/product/58056
#   - Accelerator Oscillator
#   - Accumulation/Distribution
#   - Adaptive Moving Average
#   - Alligator
#   - Average Directional Movement Index
#   - Average Directional Movement Index Wilder
#   - Average True Range
#   - Awesome Oscillator
#   - Bollinger Bands - Free
#   - Bears Power
#   - Bulls Power
#   - Chaikin Oscillator
#   - Commodity Channel Index
#   - DeMarker
#   - Double Exponential Moving Average
#   - Envelops
#   - Force Index
#   - Fractal Adaptive Moving Average
#   - Fractals
#   - Gator Oscillator
#   - Ichimoku Kinko Hyo
#   - MACD - Free
#   - Market Facilitation Index
#   - Momentum
#   - Money Flow Index
#   - Moving Average - Free
#   - Moving Average of Oscillator
#   - OBV On Balance Volume - Free
#   - Parabolic SAR
#   - Relative Strength Index
#   - Relative Vigor Index
#   - Standard Deviation
#   - Stochastic - Free
#   - Triple Exponential Average
#   - Triple Exponential Moving Average
#   - Variable Index Dynamic Average
#   - Volumes
#   - Williams' Percent Range
#
# -------------------------------------------------------------------- #

class Indicator:
    def __init__(self,
                 address='localhost',
                 port=9090,
                 listen=1):

        self.address = address
        self.port = port
        self.listen = listen
        self.location = (address, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.address, self.port))
        self.s.listen(self.listen)

    # -------------------------------------------------------------------- #
    # Paid
    symbol = "EURUSD"
    def moving_average(self,
                       symbol,
                       time_frame=1,
                       period=20,
                       start_position=0,  # Change it if you want past values, zero is the most recent.
                       # method:
                       # 0 - MODE_SMA
                       # 1 - MODE_EMA
                       # 2 - MODE_SMMA
                       # 3 - MODE_LWMA
                       method=0,
                       # applied_price:
                       # 0 - PRICE_CLOSE
                       # 1 - PRICE_OPEN
                       # 2 - PRICE_HIGH
                       # 3 - PRICE_LOW
                       # 4 - PRICE_MEDIAN
                       # 5 - PRICE_TYPICAL
                       # 6 - PRICE_WEIGHTED
                       applied_price=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"moving_average,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{period},"
                       f"{start_position},"
                       f"{method},"
                       f"{applied_price}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #
    # Paid


if __name__ == '__main__':
    print('Getting the socket ready.. Please wait ..')
    socket = Indicators()
    socket.moving_average()
    init_bot()
