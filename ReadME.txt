Scrapmart Modules:
main
userauthentication
usermanagement
shopmanagement
searchconsole
administration


Scrapmart Models:

1)userauthentication:
auth default model

2)usermanagement:
userinfo (Connected through foreign key to userid)

3)shopmanagement:
searchdb (Connected through foreign key to userid)

4)searchconsole:
city 
locality(connected through foreign key to city) 

5)main:
userquery 
