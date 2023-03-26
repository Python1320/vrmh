from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

import logging,sys,os,threading,time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
from pprint import pprint
import asyncio
import sys
from contextlib import suppress
#from asynccmd import Cmd


from os import system
system("title VRMH")

import argparse
client = SimpleUDPClient("10.0.200.204", 54321)

def clamp(num, min_value, max_value):
	return max(min(num, max_value), min_value)

brr_limit_time=False

def setBrrLevel(brrlevel,brr_limit_time_set=20):
	global brr_limit_time
	brrlevel=clamp(brrlevel,0,1.0)
	
	if brrlevel<=0:
		client.send_message("/brr", 0)
	client.send_message("/brr", brrlevel)
	if brrlevel<=0:
		brr_limit_time=False
	else:
		brr_limit_time=time.time() + brr_limit_time_set

def joyconrumble1(key,*args):
	brrlevel=float(args[0] if (type(args[0]) == int or type(args[0]) == float) else args[0][0])
	brrlevel=clamp(brrlevel*1.5-0.1,0,1.0)
	print(key,"|",args,"=>",brrlevel)
	setBrrLevel(brrlevel)

def eargrab_stretch(key,*args):
	brrlevel=float(args[0] if (type(args[0]) == int or type(args[0]) == float) else args[0][0])
	brrlevel=clamp(brrlevel,0,1.0)
	print(key,"|",args,"=>",brrlevel)
	setBrrLevel(brrlevel,1)

def eargrab(key,*args):
	brrlevel=float(args[0] if (type(args[0]) == bool) else args[0][0])
	brrlevel=clamp(brrlevel,0,1.0)
	print(key,"|",args,"=>",brrlevel)
	setBrrLevel(brrlevel,1)

dispatcher = Dispatcher()
dispatcher.map("/brr", joyconrumble1)
dispatcher.map("/avatar/parameters/joyconrumble1", joyconrumble1)
dispatcher.map("/avatar/parameters/headpats", joyconrumble1)
#dispatcher.map("/avatar/parameters/joyconrumble2", joyconrumble1)

dispatcher.map("/avatar/parameters/LeftEar_Stretch", eargrab_stretch)
dispatcher.map("/avatar/parameters/RightEar_Stretch", eargrab_stretch)

dispatcher.map("/avatar/parameters/LeftEar_IsGrabbed", eargrab)
dispatcher.map("/avatar/parameters/RightEar_IsGrabbed", eargrab)

#dispatcher.set_default_handler(print)
ip = "127.0.0.1"
port = 9001


async def loop():
	global brr_limit_time
	print("VR Microcontroller OSC Haptics v0.1")
	await asyncio.sleep(1)
	client.send_message("/brr", 1.0)
	await asyncio.sleep(1)
	client.send_message("/brr", 0.0)
	while True:
		await asyncio.sleep(0.1)
		if brr_limit_time and time.time() > brr_limit_time:
			brr_limit_time=None
			client.send_message("/brr", 0.0)
			print("Setting brr to 0")

async def init_main():
	server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
	transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
	await loop()  # Enter main loop of program

	transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
