#!/usr/bin/env python3

"""
Created on January 9 11:39:15 2016

@author: Alan Yorinks
Copyright (c) 2016 Alan Yorinks All right reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys
import signal
import argparse

from xideco.xidekit.xidekit import XideKit


class MyMonitor(XideKit):
    def __init__(self, router_ip_address=None, subscriber_port='43125', publisher_port='43124'):
        """
        This method monitors all messages going through a Xideco router.
        :param router_ip_address: Xideco Router IP Address - if not specified, it will be set to the local computer
        :param subscriber_port: Xideco router subscriber port. This must match that of the Xideco router
        :param publisher_port: Xideco router publisher port. This must match that of the Xideco router
        :return:
        """
        print('\nXiBot Monitor - monitor')

        super().__init__(router_ip_address, subscriber_port, publisher_port)

    def incoming_message_processing(self, topic, payload):
        """
        This method is overwritten in the inherited class to process the data
        :param topic: Message topic string
        :param payload: Message content
        :return:
        """
        print(topic, payload)


def start_monitor():
    """
    Main function for the monitor
    :return:
    """
    # noinspection PyShadowingNames

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', dest='router_ip_address', default='None', help='Router IP Address')

    args = parser.parse_args()
    kw_options = {}

    if args.router_ip_address != "None":
        kw_options['router_ip_address'] = args.router_ip_address

    my_mon = MyMonitor(**kw_options)
    my_mon.set_subscriber_topic('')
    my_mon.receive_loop()

    # signal handler function called when Control-C occurs
    # noinspection PyShadowingNames,PyUnusedLocal,PyUnusedLocal
    def signal_handler(signal, frame):
        print("Control-C detected. See you soon.")
        sys.exit(0)

    # listen for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":

    try:
        start_monitor()
    except KeyboardInterrupt:
        sys.exit(0)
