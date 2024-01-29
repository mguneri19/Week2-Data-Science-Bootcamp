# Görev17:  Seaborn kütüphanesi içerisinden Tipsveri setini tanımlayınız.
import pandas as pd
import seaborn as sns

df = sns.load_dataset("tips")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df.head()

# Görev18:  Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
df.groupby("time").agg({"total_bill": ["sum", "min", "max", "mean"]})
#2.alternatif
result = df.groupby("time")["total_bill"].agg(["sum", "min", "max", "mean"])

# Görev19:  Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
result =df.groupby(["day", "time"]).agg({"total_bill": ["sum", "min", "max","mean"]})
result.reset_index()

# Görev 20:  Lunch zamanına ve kadın müşterilere ait total_bill ve tip  değerlerinin day'e göre toplamını, min, max ve ortalamasını bulunuz.
lunch_females = df[(df["time"] == "Lunch") & (df["sex"] == "Female")]
a=lunch_females.groupby("day").agg({"total_bill": ["sum", "min", "max", "mean"],
                                  "tip": ["sum", "min", "max", "mean"]})
a.reset_index()

#2.alternatif
df[(df['time']=='Lunch') & (df['sex']=='Female')].groupby('day').agg({'total_bill': ['sum', 'min', 'max', 'mean'], 'tip': ['sum', 'min', 'max', 'mean']})

# Görev 21:size'i3'ten küçük, total_bill'i10'dan büyük olan siparişlerin ortalaması nedir? (loc kullanınız)

df.head()
df_new = df.loc[(df["size"] < 3) & (df["total_bill"] > 10)].select_dtypes(include=['float64', 'int64']).mean() #anlamadım, kategorical değil dedi neden? sor istersen
print(df_new)

#2.alternatif ve daha iyi çözüm
average_values = df.loc[(df["size"] < 3) & (df["total_bill"] > 10), ["size", "total_bill"]].mean()


# Görev22:  total_bill_tip_sum adında yeni bir değişken oluşturunuz. Her bir müşterinin ödediği totalbill ve tip in toplamını versin.

df["total_bill_tip_sum"] = df["total_bill"] + df["tip"]
df.head()

#2.alternatif
df["total_bill_tip_sum"] = df.apply(lambda row: row["total_bill"] + row['tip'], axis=1)
df.head()

# Görev23:  total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız.


df_sorted = df.sort_values(by='total_bill_tip_sum', ascending=False) # 'total_bill_tip_sum' sütununa göre büyükten küçüğe sıralayalım
top_30_df = df_sorted.head(30) # İlk 30 satırı yeni bir DataFrame'e atayalım
top_30_df.reset_index()
print(top_30_df)

#2.alternatif
thirty_df = df.sort_values(by="total_bill_tip_sum", ascending=False).head(30)
