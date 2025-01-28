import plistlib
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


#COMMAND HANDLING



async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		text = update.message.text.lower()
	except:
		return
	if text == "/link opencoreguide" or text == "/link opencore":
		await update.message.reply_text("Link to OpenCore guide: https://dortania.github.io/OpenCore-Install-Guide/")
	elif text == "/link weg" or text == "/link whatevergreen":
		await update.message.reply_text("Link to WhateverGreen: https://github.com/acidanthera/whatevergreen/releases")
	elif text == "/link nootedred":
		await update.message.reply_text("Link to NootedRed: https://chefkissinc.github.io/applehax/nootedred/")
	elif text == "/link opencorepkg" or text == "/link ocpkg":
		await update.message.reply_text("Link to the OpenCore Package: https://github.com/acidanthera/OpenCorePkg")
	elif text == "/creator" or text=="/dev" or text=="/developer":
		await update.message.reply_text("My developer is @Helemen7 (https://github.com/Helemen7)")
	elif text == "/link propertree":
		await update.message.reply_text("Link to ProperTree: https://github.com/corpnewt/ProperTree")
	elif text == "/link mountefi":
		await update.message.reply_text("Link to MountEFI: https://github.com/corpnewt/MountEFI")
	elif text == "/link unplugged":
		await update.message.reply_text("Link to UnPlugged: https://github.com/corpnewt/UnPlugged")
	elif text == "/link itlwm":
		await update.message.reply_text("Link to itlwm: https://github.com/OpenIntelWireless/itlwm")
	elif text == "/link hackintool":
		await update.message.reply_text("Link to HackinTool: https://github.com/benbaker76/Hackintool")   
	elif text=="/link utbmap" or text=="/link usbtoolbox":
		await update.message.reply_text("Link to UTBMap | USBToolBox: https://github.com/USBToolBox/kext")
	elif text=="/link oclp" or text=="/link legacypatcher":
		await update.message.reply_text("Link to OpenCore Legacy Patcher Guide: https://dortania.github.io/OpenCore-Legacy-Patcher/")
	elif text=="/link opcorebootcosmetics" or text=="/link boot":
		await update.message.reply_text("Link to Dortania Guide for Boot chime: https://dortania.github.io/OpenCore-Post-Install/cosmetic/gui.html#setting-up-boot-chime-with-audiodxe")
	elif text=="/link noverbose":
		await update.message.reply_text("Link to verbose remove: https://dortania.github.io/OpenCore-Post-Install/cosmetic/verbose.html#macos-decluttering")
	elif text=="/link smbios" or text=="/link gensmbios":
		await update.message.reply_text("Link to GenSMBIOS: https://github.com/corpnewt/GenSMBIOS")
	elif text=="/link gpu depth" or text=="/link gpu other" or text=="/link gpu":
		await update.message.reply_text("Link to in depth GPU patching: https://dortania.github.io/OpenCore-Post-Install/gpu-patching/#intel-igpu-patching")
	elif text=="/link gpu intel":
		await update.message.reply_text("""
Link to Intel GPU patching: http//dortania.github.io/OpenCore-Post-Install/gpu-patching/intel-patching/

PS: Read not only the first page, but all the successive ones until BusID, and follow them to detail.

""")

	elif text == "/plist help":
		await update.message.reply_text("""Use of /plist:
Respond to a .plist file (config.plist) with /plist to give important information about quirks, boot args and kexts.
""")
	elif text=="/link ssdttime":
		await update.message.reply_text("Link to SSDTTime: https://github.com/corpnewt/SSDTTime")
	elif text == "/link help":
		await update.message.reply_text("""Use of /link:
Use: /link [product]
Have the link to a package, application, ...

COMMAND LIST:
/link _:

opencoreguide -> Dortania guide
oclp / legacypatcher -> OpenCore Legacy Patcher
whatevergreen -> Whatevergreen.kext
NootedRed -> NootedRed guide
opencorepkg -> OpenCore Package
propertree -> ProperTree .plist utility
mountefi -> MountEFI disk utility
unplugged -> UnPlugged no wifi installation guide
itlwm -> itlwm.kext for Intel WiFi
hackintool -> HackinTool Hackintosh tool, useful for getting info about system and checking if everything is working fine.
ssdttime -> Tool created by corpnewt that helps you make custom ssdts
utbmap / usbtoolbox -> Tool and Kext that helps you map USB ports on your device
GenSMBIOS -> Tool to generate fake Mac serial, to make Apple applications work
gpu -> All GPU patching:
	- intel -> Intel general iGPU patching
	- depth -> In depth GPU patching
noverbose -> Remove verbose from OpenCore
boot -> After install makes boot picker look better
""")
	elif text =="/creator help" or text=="/dev help" or text=="/developer help":
		await update.message.reply_text("""
How to use /creator | dev | developer command?
/creator command gives credit to the developer and its GitHub, why don't you try xD

""")
	else:
		await update.message.reply_text(f"Command not understood err 0: {text}. If you think this command should be added, contact the developer.")



#PLIST PARSING

async def parse_plist(update: Update, context: ContextTypes.DEFAULT_TYPE):
	replied_message = update.message.reply_to_message
	# Does the message really contain a .plist file?
	try:
		if not replied_message.document:
			await update.message.reply_text("Please send me a .plist file to analyze.")
			return
	except:
		return
	
	#Downloading .plist file
	
	document: Document = replied_message.document
	file = await document.get_file()
	file_path = f"/tmp/{document.file_name}"
	await file.download_to_drive(file_path)

	if not document.file_name.endswith(".plist"):
		await update.message.reply_text("Sorry, this is not a valid config.plist.")
		return



	try:
		await update.message.reply_text("Looking at your config...")
		# Reading config.plist file using plistlib
		with open(file_path, "rb") as plist_file:
			plist_data = plistlib.load(plist_file)

		# Extracting fundamental information
		boot_args = plist_data.get("NVRAM", {}).get("Add", {}).get("7C436110-AB2A-4BBB-A880-FE41995C9F82", {}).get("boot-args", "")
		SSDTS = plist_data.get("ACPI", {}).get("Add", [])
		kexts = plist_data.get("Kernel", {}).get("Add", [])
		quirks = plist_data.get("Booter", {}).get("Quirks", {})
		drivers= plist_data.get("UEFI", {}).get("Drivers", [])
		tools=plist_data.get("Misc", {}).get("Tools", [])
		
		temp:int=0
		lenght:int=0

		# Prepairing the response
		response = ""
		response += f"Boot Args:\n{boot_args}\n\n" if boot_args else "Boot Args: Not found\n\n"
        
		
		for diz in SSDTS:
			if diz.get("Enabled")==True:
				temp+=1

		response+= f"ACPI -> Add ({temp}/{len(SSDTS)}):\n\n"
		
		temp=0	

		if SSDTS:
			for ssdt in SSDTS:
				response += f"- {ssdt.get('Path', 'No name')}\n"
		else:
			response += "No SSDT found"
			
		response += f"\nBooter -> Quirks ({len(quirks)}):\n\n"
		for quirk, value in quirks.items():
			response += f"- {quirk}: {value}\n"
		
		
		
		for diz in kexts:
			if diz.get("Enabled")==True:
				temp+=1
		response += f"\n\nKexts: ({temp}/{len(kexts)})\n"
		temp=0
		if kexts:
			for kext in kexts:
				response += f"- {kext.get('BundlePath', 'No name')}\n"
		else:
			response += "No kext found.\n"
		

		
		for diz in tools:
			if diz.get("Enabled")==True:
				temp+=1

		response+=f"\n\nMisc -> Tools ({temp}/{len(tools)}):\n"
		temp=0
		if tools:
			for tool in tools:
				response+=f"- {tool.get('Path', 'No name')}\n"
		else:
			response+="Tools not found\n"
		
		
		for diz in drivers:
			if diz.get("Enabled")==True:
				temp+=1
		response+=f"\n\nUEFI -> Drivers ({temp}/{len(drivers)})\n"
		temp=0

		if drivers:
			for driver in drivers:
				response+= f"- {driver.get('Path', 'No name')}\n"
		else:
			response+="No drivers found\n"

		await update.message.reply_text(response)

	except Exception as e:
		await update.message.reply_text(f"Error while loading your .plist: Error {str(e)}")
