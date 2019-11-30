__author__ = 'Hao'

### About the data:

## Obtaining raw data of the New Dana Classification:
# Go to: https://toolslick.com/conversion/data/html-to-json
# Fetch HTML from url: http://www.webmineral.com/dana/dana.php#.XdlAnS2ZPOQ
# In the HTML, only retain the highest-level "blockquote" and its content (which contains the whole Dana)
# Click "CONVERT" and download the JSON file.

## Obtaining raw data of the Old Dana Classfication:
# Data available at: http://www.webmineral.com/danaclass.shtml#.XdlAlC2ZPOQ
# Store the table into an XLSX file

## Obtaining IMA mineral properties from RRUFF:
# Go to: http://rruff.info/ima/
# On the left panel, in "Export Options", select all (or desired) options, and then click "DOWNLOAD CSV"

print("Hello")

import json
import csv

# File names:


# Read data from RRUFF IMA

RRUFF = []
with open("data/RRUFF_All_20191128_184220.csv", "r") as read_file:
    print("Reading RRUFF ...")
    reader = csv.DictReader(read_file)
    RRUFF = [row for row in reader]
    print("Properties of " + str(len(RRUFF)) + " minerals from RRUFF loaded. E.g.")
    print(RRUFF[0])


# Note this is "dana"
dana = {"name": "Dana Classification (All Minerals)", "children": []}

total_count = 0

with open("data/webmineral_dana.json", "r") as read_file:
    data = json.load(read_file)

    data = data["blockquote"]

    # print(type(data))

    count = 0

    for x in data:
        # print(x["h2"])
        x_blockquote = x["blockquote"]
        if isinstance(x_blockquote, dict): x_blockquote = [x_blockquote]

        x_temp = {}
        x_temp["dana-number"] = x["h2"].split(maxsplit = 1)[0]
        x_temp["dana-name"] = x["h2"].split(maxsplit = 1)[1] if len(x["h2"].split(maxsplit = 1)) > 1 else ""
        x_temp["name"] = " ".join(x["h2"].split())  # <-- NEW
        # x_temp["name"] = x["h2"]
        x_temp["children"] = []
        # print(x_temp)
        # break

        for y in x_blockquote:
            # print("    " + y["h3"])
            y_blockquote = y["blockquote"]
            if isinstance(y_blockquote, dict): y_blockquote = [y_blockquote]

            y_temp = {}
            y_temp["dana-number"] = y["h3"].split(maxsplit = 1)[0]
            y_temp["dana-name"] = y["h3"].split(maxsplit = 1)[1] if len(y["h3"].split(maxsplit = 1)) > 1 else ""
            y_temp["name"] = " ".join(y["h3"].split())  # <-- NEW
            # y_temp["name"] = y["h3"]
            y_temp["children"] = []
            # print(y_temp)

            for z in y_blockquote:
                # print("        " + z["h4"])
                z_dd = z["dd"]
                # print(z_dd)

                if isinstance(z_dd, dict): z_dd = [z_dd]

                z_temp = {}
                z_temp["dana-number"] = z["h4"].split(maxsplit = 1)[0]
                z_temp["dana-name"] = z["h4"].split(maxsplit = 1)[1] if len(z["h4"].split(maxsplit = 1)) > 1 else ""
                # print(z_temp["dana-number"])
                # print(z_temp["dana-name"])
            # z_temp["name"] = z["h4"]  # OLD -->
                z_temp["name"] = " ".join(z["h4"].split())  # <-- NEW
                # print(z_temp["name"])
                z_temp["children"] = []
                # print(z_temp)

                total_count += len(z_dd)

                for w in z_dd:
                    # print(w)
                    w_num = w["#text"]
                    w_num_marking = ""
                    if isinstance(w_num, list):
                        w_num_marking = w_num[1]
                        w_num = w_num[0]

                    w_name = w["a"]["#text"]
                    # print("            " + w_num + "    " + w_name)

                    w_temp = {}
                    w_temp["name"] = str(w_num + " " + w_name)
                    w_temp["size"] = 1
                    w_temp["webmin-mineral-name"] = w_name
                    w_temp["dana-name"] = w_name
                    w_temp["dana-number"] = w_num
                    w_temp["webmin-ima-marking"] = w_num_marking
                    w_temp["webmin-chemistry"] = w["small"]
                    w_temp["webmin-url"] = "www.webmineral.com" + w["a"]["@href"].strip(".")

                    # # Structure info from Webmineral.com; commented out to reduce output size
                    # w_temp["webmin-structure-info"] = w["span"]

                    # *** Match and add RRUFF data!
                    is_in_RRUFF = False
                    rruff_tmp = None
                    for rruff in RRUFF:
                        if w_temp["webmin-mineral-name"] == rruff["Mineral Name (plain)"]:
                            # print(w_temp["mineral-name"] + " matched with RRUFF records")
                            is_in_RRUFF = True
                            rruff_tmp = rruff
                            break
                        elif w_temp["webmin-mineral-name"] == rruff["IMA Number"]:
                            print(w_temp["webmin-mineral-name"] + " matched with RRUFF records by IMA number; IMA mineral name is " +
                                  rruff["Mineral Name (plain)"] +
                                  " and its webmineral marking is " + w_temp["webmin-ima-marking"])
                            is_in_RRUFF = True
                            rruff_tmp = rruff
                            break

                    if is_in_RRUFF:
                        #
                        w_temp["rruff-mineral-name-plain"] = rruff_tmp["Mineral Name (plain)"]
                        w_temp["rruff-mineral-name"] = rruff_tmp["Mineral Name"]
                        w_temp["rruff-mineral-name-html"] = rruff_tmp["Mineral Name (HTML)"]
                        #
                        w_temp["rruff-chemistry-html"] = rruff_tmp["RRUFF Chemistry (HTML)"]
                        w_temp["rruff-chemistry-plain"] = rruff_tmp["RRUFF Chemistry (plain)"]
                        #
                        w_temp["rruff-ima-number"] = rruff_tmp["IMA Number"]
                        w_temp["rruff-crystal-systems"] = rruff_tmp["Crystal Systems"]
                        w_temp["rruff-oldest-known-age"] = rruff_tmp["Oldest Known Age (Ma)"]
                        w_temp["rruff-elements"] = rruff_tmp["Chemistry Elements"]


                    if is_in_RRUFF == False:
                        # print(w_temp["dana-number"] + " " + w_temp["webmin-mineral-name"] + " is not found in RRUFF" +
                        #       " and its webmineral marking is " + w_temp["webmin-ima-marking"])
                        pass


                    # print(json.dumps(w_temp, indent=4, sort_keys=True))
                    z_temp["children"].append(w_temp)

                    # break

                # print(json.dumps(z_temp, indent=4, sort_keys=True))
                y_temp["children"].append(z_temp)
                # break

            # print(json.dumps(y_temp, indent=4, sort_keys=True))
            x_temp["children"].append(y_temp)

        # print(json.dumps(x_temp, indent=4, sort_keys=True))
        # write_file.write(json.dumps(x_temp, indent=4, sort_keys=True) + ",\n")
        dana["children"].append(x_temp)

        count += 1
        if count >= 100: break

write_file = open("dana2.json", "w+")
write_file.write(json.dumps(dana, indent=2, sort_keys=True))
write_file.close()

print("Total in Webmineral: " + str(total_count))
# Add old dana information on top

old_dana = {"name": "Dana Classification", "children": []}

skip_count = 0


with open("old_vs_new_dana.csv", "r") as read_old_dana:

    reader = csv.reader(read_old_dana)

    is_silicates = False

    for row in csv.reader(read_old_dana):
        if skip_count == 0:
            skip_count += 1
            continue

        category_now = ""
        if not is_silicates:
            if row[0].strip() != "":
                # print(row)
                category_now = row[0].strip().split("\u00a0")[-1]
                category_num = row[0].strip().split("\u00a0")[0]
                old_dana["children"].append({
                    "name": category_num + ". " + category_now,
                    "children": [],
                    "dana-number": category_num,
                    "dana-name": category_now
                })
                # old_dana["children"].append({"name": category_num + " - " + category_now, "children": []})
                # print(category_now)

                if row[1].strip() != "":
                    is_silicates = False
                    old_dana["children"][-1]["children"].append(
                        {"name": row[1].strip().split("\u00a0")[1], "children": []}
                    )
                    # print(old_dana["children"][-1]["children"])
                else:   # Means it's the silicates now
                    is_silicates = True
            else:
                old_dana["children"][-1]["children"].append(
                    {"name": row[1].strip().split("\u00a0")[1], "children": []}
                )
                # print(old_dana["children"][-1]["children"])

        else:
        # if is_silicates:
            if row[0].strip() != "":
                category_now = row[0].strip().split("\u00a0")[-1]
                print(category_now)
                # print(json.dumps(old_dana["children"][-1], indent=2, sort_keys=True))
                old_dana["children"][-1]["children"].append(
                    {"name": category_now, "children": []}
                )
                # print(json.dumps(old_dana["children"][-1], indent=2, sort_keys=True))
                if row[1].strip() != "":
                    old_dana["children"][-1]["children"][-1]["children"].append(
                        {"name": row[1].strip().split("\u00a0")[1], "children": []}
                    )
                else:   # Means it's the silicates now
                    pass
            else:
                old_dana["children"][-1]["children"][-1]["children"].append(
                    {"name": row[1].strip().split("\u00a0")[1], "children": []}
                )

                # old_dana["children"][-1]


        # print(row[0].strip())
        # print(row[1].strip())
    # mydict = {rows[0]:rows[1] for rows in reader}

print(json.dumps(old_dana, indent=4, sort_keys=True))

for x in old_dana["children"]:
    if "Silicates" not in x["name"]:

        print(x["name"])
        for y in x["children"]:
            # print(y)
            for k in dana["children"]:
                # print(k["name"].replace("-", "   ").split()[0])
                # print(y["name"].split()[0])
                if k["name"][:3] == y["name"][:3] or k["name"].split()[0] == y["name"].split()[0]:
                    # print(k)
                    y["name"] = k["name"]
                    y["children"] = k["children"]
                    y["dana-number"] = y["name"].split()[0]
                    y["dana-name"] = y["name"].split()[1]
                    break

    else:
        print(x["name"])

        for y in x["children"]:
            print(y["name"])
            for z in y["children"]:
                print(z)
                # print(json.dumps(dana["children"], indent=2, sort_keys=True))
                for k in dana["children"]:
                    # print(k["name"])
                    # print(k["name"].replace("-", "   ").split()[0])
                    # print(y["name"].split()[0])
                    if k["name"][:3] == z["name"][:3] or k["name"].split()[0] == z["name"].split()[0]:
                        print("yay")
                        z["name"] = k["name"]
                        z["children"] = k["children"]
                        z["dana-number"] = z["name"].split()[0]
                        z["dana-name"] = z["name"].split()[1]
                        break

# print(json.dumps(old_dana, indent=2, sort_keys=True))

# Write to JSON file
write_file = open("dana.json", "w+")
write_file.write(json.dumps(old_dana, indent=2, sort_keys=True))
write_file.close()

# Write to a Javascript file starting with "var dana ="
write_file = open("dana.js", "w+")
write_file.write("var dana = ")
write_file.write(json.dumps(old_dana, indent=2, sort_keys=True))
write_file.close()


print("    World!")

