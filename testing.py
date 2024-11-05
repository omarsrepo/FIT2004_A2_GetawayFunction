yn = (46.8, 27.8, 32.5, 39.5, 32.8, 31.0, 26.2, 20.8)
yd = (33.6, 23.3, 43.1, 31.0, 30.5, 38.0, 30.1, 25.8)

yn_avg = sum(yn)/len(yn)
yd_avg = sum(yd)/len(yd)


sum1 = 0
for value in yn:
    sum1 += (value - yn_avg)**2
print(sum1/7)

sum2 = 0
for value in yd:
    sum2 += (value - yd_avg)**2
print(sum2/7)
