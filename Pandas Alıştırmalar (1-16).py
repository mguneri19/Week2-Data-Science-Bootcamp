# Görev1:  Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız
import pandas as pd
import seaborn as sns

df = sns.load_dataset("titanic")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df.head()

# Görev2:  Titanic verisetindeki kadın ve erkek yolcuların sayısını bulunuz.
df["sex"].value_counts()

# Görev3:  Her bir sutuna ait unique değerlerin sayısını bulunuz.
df.nunique()

# Görev4:  pclass değişkeninin unique değerlerinin sayısını bulunuz.
df["pclass"].nunique()

# Görev5:  pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
df[["pclass", "parch"]].nunique()  # dikkat birden fazla değişkenin içine çift parantez ile göster

# Görev6:  embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz ve tekrar kontrol ediniz.
df["embarked"].info()
df["embarked"] = df["embarked"].astype("category")  # kaydetmen gerekiyor ki çevirebilirsin.
df["embarked"].info()

# Görev7:  embarked değeri C olanların tüm bilgelerini gösteriniz.
df.loc[df["embarked"] == "C"]

# Görev8:  embarked değeri S olmayanların tüm bilgelerini gösteriniz.
df.loc[(df["embarked"] == "C") | (df["embarked"] == "Q")]  # 3 tane embarked şehir olduğunu biliyorum, bu yüzden C veya Q dedim


df.loc[ df["embarked"] != "S"] #2. alternatif

embarked_not_s = df[df['embarked'] != 'S'] #3. alternatif

# Görev9:   Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
df.loc[(df["age"] < 30) & (df["sex"] == "female")]

# Görev10:  Fare'i 500'den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
df.loc[(df["fare"] > 500) | (df["age"] > 70)]

# Görev 11:  Her bir değişkendeki boş değerlerin toplamını bulunuz.
df.isnull().sum()  # ayrı ayrı tüm değişkenlerde olan boşları buluyor ve her bir gözlem değeri için topluyor ve toplam boş değeri buluyorum.

# Görev 12:  who değişkenini dataframe’den çıkarınız.
df.drop("who",axis=1, inplace=True)
df.head()


# Görev13:  deck değişkenindeki boş değerleri deck değişkenin en çok tekrar eden değeri(mode) ile doldurunuz.
df["deck"].mode()[0] #modun 0. dediğimizde modlar arasında en frekansı büyük yani serinin moduna ulaşmış oluyoruz. Burası için C değeri
df["deck"].isnull().sum() #688 tane boş var.
df["deck"].fillna(value="C", inplace=True) #688 tane boş değeri mod değeri ile doldurdum.
df["deck"].isnull().sum() #tekrar kontrol ediyorum, toplam sıfır boş değer var.

#2. alternatif
deck_mode = df['deck'].mode()[0]
df['deck']= df['deck'].apply(lambda x: deck_mode if pd.isnull(x) else x )
print(df['deck'])

#3. alternatif
df_filled_deck = df["deck"].fillna(df["deck"].mode().iloc[0])
print(df)

# Görev14:  age değişkenindeki boş değerleri age değişkenin medyanı ile doldurunuz.
df["age"].median() #medyan değeri 28.0
df["age"].isnull().sum() #177 boş değeri medyan ile dolduracağım.
df["age"].fillna(value=28, inplace=True)
df["age"].isnull().sum() #tekrar kontrol ediyorum, toplam sıfır boş değer var.


# Görev15:  survived değişkeninin pclass ve cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz.
df.pivot_table("survived", "pclass","sex", aggfunc=["sum", "count", "mean"])

#2.alternatif
survived_analysis = df.groupby(["sex", "pclass"]).agg({"survived": ["sum", "count", "mean"]})

df.groupby(['pclass', 'sex'])['survived'].agg(['sum', 'count', 'mean'])

# Görev16:  30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazın.
# Yazdığınız fonksiyonu kullanarak titanik verisetinde age_flag adında bir değişken oluşturunuz. (apply ve lambda yapılarını kullanınız)


df["age_flag"] = df.loc[:,df.columns.str.contains("age")].apply(lambda x: 1 if x < 30 else 0) #neden olmaz?

#2.alternatif
df["age_flag"] = df.loc[:, df.columns[df.columns.str.contains("age")]].apply(lambda x: x.apply(lambda y: 1 if y < 30 else 0))

df["age_flag"] = df["age"].apply(lambda x: 1 if x < 30 else 0)
df.head()


