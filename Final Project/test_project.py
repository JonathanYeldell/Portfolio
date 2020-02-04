
import final_supreme as proj

# Test #1 [Get Page FUNCTION]
results = proj.get_page()

if 'html' in results:
    value = True

assert (value == True), 'HTML request failed.'
# Test #1 [Get Page FUNCTION]


#Test 2 Build product list FUNCTION
page = proj.get_page()
testing_list = []

Product_objects = proj.build_product_list(page)

raw_product_link = page.findAll("div", {"class": "inner-article"})

for links in raw_product_link:

    product_link = "https://www.supremenewyork.com" + links.a["href"]

    testing_list.append(product_link)

assert (len(Product_objects) == len(testing_list))
#Test 2 Build product list FUNCTION


#Test 3 Get description FUNCTION
old_list = proj.build_product_list(page)

descriptions = proj.get_descriptions(old_list)

assert (len(descriptions)==len(Product_objects))
#Test 3 Get description FUNCTION


# Test 4 THIS CODE TESTS THE MONITOR/ALERT FUNCTION
p1 = proj.Product('link1', 'a', True)
p2 = proj.Product('link2', 'https://assets.supremenewyork.com/169782/vi/0KGxa8QUSW4.jpg', True)
p3 = proj.Product('link2', 'https://assets.supremenewyork.com/169782/vi/0KGxa8QUSW4.jpg', False)

old_list = [p1, p2]
new_list = [p1, p3]

all_descriptions = {
    'link1': 'description',
    'link2': 'another description'
}

proj.monitor(old_list,new_list,proj.webhook_url,all_descriptions)
# Test 4 THIS CODE TESTS THE MONITOR/ALERT FUNCTION

print('Yee Haw, The code passes ALL tests!')
