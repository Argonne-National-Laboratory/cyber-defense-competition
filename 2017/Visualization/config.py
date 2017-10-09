from collections import OrderedDict

prefix = "10.10.20."
red_range = []
green_range = []
for i in range(23, 33):
    red_range.append(i)
for i in range(190, 201):
    red_range.append(i)
for i in range(216, 255):
    red_range.append(i)

for i in range(200,216):
    green_range.append(i)



cdc = [
    {"num": 1, "name": "Dakota State"},
    {"num": 2, "name": "Governors State"},
    {"num": 3, "name": "Indiana Tech"},
    {"num": 4, "name": "Indiana University"},
    {"num": 5, "name": "Iowa State"},
    {"num": 6, "name": "John A Logan"},
    {"num": 7, "name": "Kansas State"},
    {"num": 8, "name": "Lewis"},
    {"num": 9, "name": "Southern Methodist"},
    {"num": 10, "name": "St. Johns"},
    {"num": 11, "name": "Central Florida"},
    {"num": 12, "name": "UIC"},
    {"num": 13, "name": "UIUC"},
    {"num": 14, "name": "Northern Iowa"},
    {"num": 15, "name": "Wright State"},
]

blue = {
    "File Server": "30",
    "Active Directory": "40",
    "HMI": "50",
    "Mail Server": "60",
    "Web Server": "70",
    "ESXi" : "2",
}

def getPrefix(team_num):
    return "10.0.%d0" % team_num

def getNetwork(team_num):
    return "%s.%s" % (getPrefix(team_num), "0")

def is_red(last_oct):
    if int(last_oct) in red_range:
        return True
    else:
        return False

def is_green(last_oct):
    if int(last_oct) in green_range:
        return True
    else:
        return False

# this is gettable from twisted while we're running
teamnets = []
for i in range(1, 16):
  teamnets.append(getNetwork(i))

line_ids = OrderedDict()
line_ids["10.0.50.60"] = "l0"
line_ids["10.0.110.30"] = "l1"
line_ids["10.0.140.70"] = "l2"
line_ids["10.0.110.2"] = "l3"
line_ids["10.0.20.70"] = "l4"
line_ids["10.0.140.30"] = "l5"
line_ids["10.0.120.50"] = "l6"
line_ids["10.0.120.30"] = "l7"
line_ids["10.0.120.70"] = "l8"
line_ids["10.0.120.60"] = "l9"
line_ids["10.0.120.40"] = "l10"
line_ids["10.0.120.2"] = "l11"
line_ids["UIC"] = "l12"
line_ids["10.0.90.2"] = "l13"
line_ids["10.0.50.2"] = "l14"
line_ids["10.0.60.30"] = "l15"
line_ids["10.0.80.2"] = "l16"
line_ids["10.0.110.40"] = "l17"
line_ids["10.0.90.40"] = "l18"
line_ids["10.0.130.30"] = "l19"
line_ids["10.20.50.70"] = "l20"
line_ids["10.0.20.60"] = "l21"
line_ids["10.0.70.30"] = "l22"
line_ids["10.0.140.40"] = "l23"
line_ids["10.0.30.60"] = "l24"
line_ids["10.0.90.30"] = "l25"
line_ids["10.0.150.40"] = "l26"
line_ids["10.0.90.50"] = "l27"
line_ids["10.0.40.2"] = "l28"
line_ids["10.0.110.60"] = "l29"
line_ids["10.0.110.70"] = "l30"
line_ids["10.0.110.50"] = "l31"
line_ids["Central Florida"] = "l32"
line_ids["10.0.100.30"] = "l33"
line_ids["10.0.150.70"] = "l34"
line_ids["10.0.130.2"] = "l35"
line_ids["10.0.30.40"] = "l36"
line_ids["10.0.30.50"] = "l37"
line_ids["10.0.30.70"] = "l38"
line_ids["20.0.30.2"] = "l39"
line_ids["10.0.30.30"] = "l40"
line_ids["Indiana Tech"] = "l41"
line_ids["10.0.140.50"] = "l42"
line_ids["10.0.10.60"] = "l43"
line_ids["10.0.80.70"] = "l44"
line_ids["10.0.60.50"] = "l45"
line_ids["10.0.150.30"] = "l46"
line_ids["10.0.40.70"] = "l47"
line_ids["10.0.140.70"] = "l48"
line_ids["10.0.90.60"] = "l49"
line_ids["10.0.130.70"] = "l50"
line_ids["10.0.130.60"] = "l51"
line_ids["10.0.130.40"] = "l52"
line_ids["UIUC"] = "l53"
line_ids["10.0.130.50"] = "l54"
line_ids["10.0.100.2 "] = "l55"
line_ids["10.0.100.60"] = "l56"
line_ids["10.0.100.70"] = "l57"
line_ids["10.0.100.50"] = "l58"
line_ids["St. Johns"] = "l59"
line_ids["10.0.100.40"] = "l60"
line_ids["10.0.50.30"] = "l61"
line_ids["10.0.50.50"] = "l62"
line_ids["10.0.50.40"] = "l63"
line_ids["Iowa State"] = "l64"
line_ids["10.0.80.60"] = "l65"
line_ids["10.0.60.40"] = "l66"
line_ids["10.0.40.60"] = "l67"
line_ids["10.0.70.2"] = "l68"
line_ids["10.0.20.30"] = "l69"
line_ids["10.0.20.60"] = "l70"
line_ids["10.0.60.70"] = "l71"
line_ids["10.0.70.60"] = "l72"
line_ids["10.0.40.50"] = "l73"
line_ids["10.0.80.50"] = "l74"
line_ids["10.0.90.70"] = "l75"
line_ids["Southern Methodist "] = "l76"
line_ids["10.0.10.30"] = "l77"
line_ids["10.0.60.60"] = "l78"
line_ids["10.0.6.2"] = "l79"
line_ids["John A Logan"] = "l80"
line_ids["10.0.70.70"] = "l81"
line_ids["10.0.80.40"] = "l82"
line_ids["10.0.150.60"] = "l83"
line_ids["10.0.150.50"] = "l84"
line_ids["10.0.150.2"] = "l85"
line_ids["Wright State"] = "l86"
line_ids["10.0.10.70"] = "l87"
line_ids["10.0.10.50"] = "l88"
line_ids["10.0.10.40"] = "l89"
line_ids["10.0.10.2"] = "l90"
line_ids["Dakota State"] = "l91"
line_ids["10.0.40.40"] = "l92"
line_ids["10.0.140.60"] = "l93"
line_ids["10.0.20.2"] = "l94"
line_ids["10.0.20.50"] = "l95"
line_ids["Governors State"] = "l96"
line_ids["10.0.70.40"] = "l97"
line_ids["10.0.80.30"] = "l98"
line_ids["Northern Iowa"] = "l99"
line_ids["10.0.40.30"] = "l100"
line_ids["Indiana University"] = "l101"
line_ids["Lewis University"] = "l102"
line_ids["Kansas State"] = "l103"
line_ids["10.0.70.50"] = "l104"

node_ids = OrderedDict()
node_ids["10.0.100.2"] = "n1"
node_ids["10.0.100.30"] = "n2"
node_ids["10.0.100.40"] = "n3"
node_ids["10.0.100.50"] = "n4"
node_ids["10.0.100.60"] = "n5"
node_ids["10.0.100.70"] = "n6"
node_ids["10.0.10.2"] = "n7"
node_ids["10.0.10.30"] = "n8"
node_ids["10.0.10.40"] = "n9"
node_ids["10.0.10.50"] = "n10"
node_ids["10.0.10.60"] = "n11"
node_ids["10.0.10.70"] = "n12"
node_ids["10.0.110.2"] = "n13"
node_ids["10.0.110.30"] = "n14"
node_ids["10.0.110.40"] = "n15"
node_ids["10.0.110.50"] = "n16"
node_ids["10.0.110.60"] = "n17"
node_ids["10.0.110.70"] = "n18"
node_ids["10.0.120.2"] = "n19"
node_ids["10.0.120.30"] = "n20"
node_ids["10.0.120.40"] = "n21"
node_ids["10.0.120.50"] = "n22"
node_ids["10.0.120.60"] = "n23"
node_ids["10.0.120.70"] = "n24"
node_ids["10.0.130.2"] = "n25"
node_ids["10.0.130.30"] = "n26"
node_ids["10.0.130.40"] = "n27"
node_ids["10.0.130.50"] = "n28"
node_ids["10.0.130.60"] = "n29"
node_ids["10.0.130.70"] = "n30"
node_ids["10.0.140.2"] = "n31"
node_ids["10.0.140.30"] = "n32"
node_ids["10.0.140.40"] = "n33"
node_ids["10.0.140.50"] = "n34"
node_ids["10.0.140.60"] = "n35"
node_ids["10.0.140.70"] = "n36"
node_ids["10.0.150.2"] = "n37"
node_ids["10.0.150.30"] = "n38"
node_ids["10.0.150.40"] = "n39"
node_ids["10.0.150.50"] = "n40"
node_ids["10.0.150.60"] = "n41"
node_ids["10.0.150.70"] = "n42"
node_ids["10.0.20.2"] = "n43"
node_ids["10.0.20.30"] = "n44"
node_ids["10.0.20.40"] = "n45"
node_ids["10.0.20.50"] = "n46"
node_ids["10.0.20.60"] = "n47"
node_ids["10.0.20.70"] = "n48"
node_ids["10.0.30.2"] = "n49"
node_ids["10.0.30.30"] = "n50"
node_ids["10.0.30.40"] = "n51"
node_ids["10.0.30.50"] = "n52"
node_ids["10.0.30.60"] = "n53"
node_ids["10.0.30.70"] = "n54"
node_ids["10.0.40.2"] = "n55"
node_ids["10.0.40.30"] = "n56"
node_ids["10.0.40.40"] = "n57"
node_ids["10.0.40.50"] = "n58"
node_ids["10.0.40.60"] = "n59"
node_ids["10.0.40.70"] = "n60"
node_ids["10.0.50.2"] = "n61"
node_ids["10.0.50.30"] = "n62"
node_ids["10.0.50.40"] = "n63"
node_ids["10.0.50.50"] = "n64"
node_ids["10.0.50.60"] = "n65"
node_ids["10.0.50.70"] = "n66"
node_ids["10.0.60.2"] = "n67"
node_ids["10.0.60.30"] = "n68"
node_ids["10.0.60.40"] = "n69"
node_ids["10.0.60.50"] = "n70"
node_ids["10.0.60.60"] = "n71"
node_ids["10.0.60.70"] = "n72"
node_ids["10.0.70.2"] = "n73"
node_ids["10.0.70.30"] = "n74"
node_ids["10.0.70.40"] = "n75"
node_ids["10.0.70.50"] = "n76"
node_ids["10.0.70.60"] = "n77"
node_ids["10.0.70.70"] = "n78"
node_ids["10.0.80.2"] = "n79"
node_ids["10.0.80.30"] = "n80"
node_ids["10.0.80.40"] = "n81"
node_ids["10.0.80.50"] = "n82"
node_ids["10.0.80.60"] = "n83"
node_ids["10.0.80.70"] = "n84"
node_ids["10.0.90.2"] = "n85"
node_ids["10.0.90.30"] = "n86"
node_ids["10.0.90.40"] = "n87"
node_ids["10.0.90.50"] = "n88"
node_ids["10.0.90.60"] = "n89"
node_ids["10.0.90.70"] = "n90"
node_ids["10.0.90.70"] = "n91"
node_ids["Central Florida"] = "n92"
node_ids["Dakota State"] = "n93"
node_ids["Governors State"] = "n94"
node_ids["Indiana Tech"] = "n95"
node_ids["Indiana University"] = "n96"
node_ids["Iowa State"] = "n97"
node_ids["John A Logan"] = "n98"
node_ids["Kansas State"] = "n99"
node_ids["Lewis"] = "n100"
node_ids["Northern Iowa"] = "n101"
node_ids["Southern Methodist"] = "n102"
node_ids["St. Johns"] = "n103"
node_ids["UIC"] = "n104"
node_ids["UIUC"] = "n105"
node_ids["Wright State"] = "n106"
