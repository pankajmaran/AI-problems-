#INPUT FORMAT - firstname.secondname@mail.com

emailid = input("Enter Email: ") 
ind = emailid.index(".") 
at = emailid.index("@") 
fname = emailid[0:ind] 
lname = emailid[ind+1:at] 
domain = emailid[at+1:] 
print("First Name: ",fname) 
print("Last Name: ",lname) 
print("Host Name: ",domain)
