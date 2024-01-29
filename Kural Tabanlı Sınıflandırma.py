#Görev1
#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
df = pd.read_csv(r"C:\Users\muhammet.guneri\Desktop\persona.csv") #dosya yolunu kopyaladım, r koymayı unutma başına
print(df)

#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df.nunique()
for col in df.columns:
    print(f"{col} sütununun frekansları:")
    print(df[col].value_counts())
    print("\n")

#Soru 3:Kaç unique PRICE vardır?
df["PRICE"].nunique() #6 tane eşsiz değer var.

#Soru 4:Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
print("PRICE sütununun frekansları:")
print(df["PRICE"].value_counts())
print("\n")

#Soru 5:Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()


#Soru 6:Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()


#Soru 7:SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()


# Soru 8:Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY")["PRICE"].mean()

# Soru 9:SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].mean()


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"])["PRICE"].mean()

#Görev2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
pd.set_option('display.max_rows', 10)
df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].mean()

#2.alternatif (daha iyi çözüm)
df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE'], as_index=False)['PRICE'].mean()

#Görev 3:  Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].mean()
agg_df.sort_values(ascending=False) #PRICE'a göre azalan sıralamasını yaptık.



#Görev 4:  Indekste yer alan isimleri değişken ismine çeviriniz.

agg_df.reset_index()
agg_df = agg_df.reset_index()
agg_df.head()
#agg_df artık gruplama yapılan sütunları da normal sütunlar olarak içerir ve herhangi bir indeksi yoktur.
# Bu işlemden sonra, agg_df üzerinde istediğiniz analizleri yapabilir, verileri görselleştirebilir veya başka işlemler
# gerçekleştirebilirsiniz.Örneğin, verileri bir dosyaya kaydedebilir, istatistiksel analizler yapabilir
# veya veri setini makine öğrenimi modellerinde kullanabilirsiniz.

#Görev 5:  Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"]) # AGE_CAT adında bir segment oluşturduk
print(agg_df)


#Görev 6:  Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
for col in agg_df.select_dtypes(include=["object"]).columns:
    agg_df[col] = agg_df[col].str.upper() #tüm kategoriklerin verisini büyütüyorum.
agg_df.head()

agg_df["customers_level_based"] = (agg_df["COUNTRY"].astype(str) + "_" + #customer level based değişkenini ekledim
                                   agg_df["SOURCE"].astype(str) + "_" +
                                   agg_df["SEX"].astype(str) + "_" +
                                   agg_df["AGE_CAT"].astype(str)).str.upper()

agg_df.head()

#2.ALTERNATİF#### (daha iyi çözüm)
col_level = ["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]
agg_df["customer_level_based"] = agg_df.apply(lambda row: '_'.join(row[col].upper() for col in col_level), axis=1)
print(agg_df)
#######

price_means = agg_df.groupby("customers_level_based")["PRICE"].mean() #istediğim çıktı oluyor ama PRICE sütun başlığı yazmıyordu, bu nedenle farklı bir adla atama yaptım.

agg_df = price_means.reset_index(name='PRICE') #sonra atama yaptığım yerde işlemin adını koyuyorum, PRICE diye

print(agg_df)


#Görev 7:  Yeni müşterileri (personaları) segmentlere ayırınız
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
print(agg_df)

agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})


#Görev 8:  Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini  tahmin ediniz

new_user = ["TUR_ANDROID_FEMALE_31_40", "FRA_IOS_FEMALE_31_40"] # yeni kullanıcılarım; 33 yaşında ANDROID kullanan bir Türk kadını ve 35 yaşında IOS kullanan bir Fransız kadını

selected_users = agg_df[agg_df["customers_level_based"].isin(new_user)]

print(selected_users) # Türk olanın Price= 41.8, Segment'i A, Fransız olanın price=32.8 segment'i C


#2.Alternatif
agg_df[agg_df['customers_level_based'].str.contains("TUR_ANDROID_FEMALE_31_40")]['PRICE'].mean()
agg_df[agg_df['customers_level_based'].str.contains("FRA_IOS_FEMALE_31_40")]['PRICE'].mean()