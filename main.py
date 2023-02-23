from flet import *
import midtransclient
import webbrowser
import jinja2
import os
import random
import string





# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    server_key='YOU server KEY HERE !!!!!!',
    client_key='YOU CLIENT KEY HEREE !!!!'
)
def main(page:Page):

	price = Text("1200",size=25,weight="bold")
	mycounter = Text("1",size=25,weight="bold")
	totalprice = Text("",size=25,weight="bold")

	youname = TextField(label="you name")
	youemail = TextField(label="email")
	youphone = TextField(label="phone")

	def calculatetotal()->str:
		# IF THE COUNTER < 1 THEN SET MYCOUNTER TO 1
		# not example -5 is NOT 
		if mycounter.value is None or price.value is None or int(mycounter.value) < 1:
			mycounter.value = 1
			return f"{1 * int(price.value)}"
		return f"{int(mycounter.value) * int(price.value)}"
		page.update()

	def decrementbtn(e):
		assert mycounter.value is not None
		mycounter.value  = f"{int(mycounter.value) - 1}"
		totalprice.value = calculatetotal()
		print("price : ",totalprice.value)
		print("you counter : ",mycounter.value)
		page.update()

	def incrementbtn(e):
		assert mycounter.value is not None
		mycounter.value  = f"{int(mycounter.value) + 1}"
		totalprice.value = calculatetotal()
		print("price : ",totalprice.value)
		print("you counter : ",mycounter.value)
		page.update()

	def buynow(e):
		random_uid = ''.join(random.choices(string.ascii_letters + string.digits,k=10))
		param = {
		    "transaction_details": {
		        "gross_amount": totalprice.value,
		        "order_id": random_uid,
		    },
		    "credit_card":{
		        "secure":True
		    },
		    # ADD CUSTOMER BIO 
		    "customer_details": {
		      "first_name": youname.value,
		      "last_name": "",
		      "email": youemail.value,
		      "phone": youphone.value
		    }
		}
		transaction = snap.create_transaction(param)
		transaction_token = transaction['token']
		print("YOu token for buy is ",transaction_token)
		env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
		template = env.get_template("index.html")
		# THEN INDEX.html WILL COPY TO PAYMENT.html
		# THEN CHANGE SNAP TOKEN ONLY
		# FOR BUY
		rendered = template.render(json_data={'snap_token':transaction_token})

		# AND OPEN PAYMENT.html
		with open("payment.html","w") as f:
			f.write(rendered)
		with open("payment.html","r") as f:
			content = f.read()
			# AND CHANGE VARIABLE TOKEN 
			content = content.replace('econst snap_token = "";',f'const snap_token ="{transaction_token}";')
		with open("payment.html","w") as f:
			f.write(content)


		# AND THEN OPEN BROWSER AUTOMATYCALY WHEN YOU CLICK BUY
		# I AM USING FIREFOX BY DEFAULT 
		browser = webbrowser.get("firefox")
		browser.open("file://"+ os.path.realpath("payment.html"))

		# AND HIDE DIALOG 
		dialog.open = False

		# AND SHOW SNACK BAR FOR OPENING BROWSER
		page.snack_bar = SnackBar(
			Text("opening browser .....!! GUYS",size=25,
				color="white"
				),
			bgcolor="green"
			)	
		page.snack_bar.open = True
		page.update()




	# NOW CREATE DIALOG IF YOU CLICK PAY NOW THEN SHOW DILOG
	dialog = AlertDialog(
		title=Text("complete you data",size=25,
			weight="bold"
			),
		content=Column([
			youname,
			youemail,
			youphone,
			Row([
				Text("Total Price : ",size=25),
				totalprice,
				],alignment="spaceBetween")
			]),
		actions=[
		ElevatedButton("Buy",
			bgcolor="blue",color="white",
			on_click=buynow

			)
		],
		actions_alignment="end"

		)

	def completeregistration(e):
		page.dialog = dialog
		dialog.open = True
		page.update()


	page.add(
	AppBar(
		title=Text("Flet Shopping",size=30,
			color="white"
			),
		bgcolor="blue"
		),

	Column([
		Image("assets/sale.jpg"),
		Text(f"price is : ${price.value}",size=25,weight="bold"),
		Text("buy this clothes",weight="bold",size=25),
		Row([
			IconButton("remove",
				bgcolor="red200",
				on_click=decrementbtn
				),
			mycounter,
			IconButton("add",
				bgcolor="blue200",
				on_click=incrementbtn
				),

			],alignment="spaceBetween"),
		ElevatedButton("pay now",
			bgcolor="blue",
			color="white",
			on_click=completeregistration

			)

		])

		)

# AND PHOTO TO ASSETS FOLDER 
flet.app(target=main,assets_dir="assets")
