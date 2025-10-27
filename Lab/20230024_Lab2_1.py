input_money = int(input("투입한 돈: "))
price = int(input("물건값: "))
money_left = input_money - price
print("")
print("거스름돈: %d원" % money_left)
print("500원짜리: %d개" % (money_left//500))
print("100원짜리: %d개" % ((money_left%500)/100))