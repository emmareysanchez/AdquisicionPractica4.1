from cProfile import label
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import seaborn as sns
import re
    
#creo una funcion usando regex para que le quite el tamaño a cada nombre de pizza para así poder unificarlas para hallar la popularidad 
def quitar_tamano(pizza):
    patron = '_[a-z]+$'
    pizza = re.sub(patron, '', pizza)
    return pizza
#cargo los csv con los que voy a trabajar
df_total = pd.read_csv('order_details_mejorado.csv')
df_order_details_orig = pd.read_csv('order_details_limpio.csv')
df_pizza_types = pd.read_csv('pizza_types.csv')
#creo un nuevo dataframe que contenga cada tipo de pizza y el número total de ventas de dicha pizza asociado
df_popularidad_pizza = pd.DataFrame()

for i in range(len(df_order_details_orig)):
    pizza = df_order_details_orig['pizza_id'][i]
    df_order_details_orig['pizza_id'][i] = quitar_tamano(pizza)

df_popularidad_pizza = df_order_details_orig[['pizza_id', 'quantity']].groupby('pizza_id').sum()
df_popularidad_pizza = df_popularidad_pizza.sort_values('quantity')
df_prediccion_final = pd.read_csv('prediccion_final.csv')



TITLE = '\n\n\n\nMAVEN PIZZA REPORT'
#creo el pdf
pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_font('helvetica', 'B',35)
pdf.set_margins(30,25,25)
pdf.set_auto_page_break(True, 25)
pdf.multi_cell(0, 10, txt=TITLE, align="C")
pdf.ln()
#añado la imagen
pdf.image('fotopizza.jpeg', x = 50, w = 100)
pdf.ln()
pdf.set_font('helvetica','', 15)
pdf.multi_cell(0, 10, txt = 'Emma Rey Sánchez\nUniversidad Pontificia Comillas ICAI', align = 'C')
#siguiente página
#creo un gráfico de barras cuyo eje x son todos los ingredientes y el eje y las cantidades de dichos ingredientes que se deben comprar para el stock de 1 semana
pdf.add_page()
pdf.set_font('helvetica', 'B', 12)
pdf.multi_cell(0, 10, txt = 'COMPARACIÓN DE COMPRA DE INGREDIENTES SEMANAL BASADOS EN LA PREDICCIÓN', align= 'C')
pdf.ln()
y = df_prediccion_final['cantidad']
x = df_prediccion_final['ingredientes']
plt.figure(figsize=(15,10))
sns.barplot(x=x, y=y)
plt.xticks(rotation = -90)
plt.savefig('grafico1.png', bbox_inches = 'tight')
pdf.image('grafico1.png', x = 8, w = 190)
pdf.ln()
pdf.ln()
pdf.set_font('helvetica', '', 12)
pdf.multi_cell(0, 10, txt = 'Como podemos observar en el gráfico superior, los ingredientes que más se usan, y por tanto, hay que comprar en cantidades más grandes, son tomates, cebollas y ajos.')
#siguiente página
# uso el dataframe df_popularidad_pizza previamente creado para crear un gráfico de barras y hallar las pizzas más y menos populares
pdf.add_page()
pdf.ln()
pdf.set_font('helvetica', 'B', 12)
pdf.multi_cell(0, 10, txt = 'CANTIDAD DE PIZZAS VENDIDAS EN 2016', align= 'C')
pdf.ln()
x = df_popularidad_pizza.index
y = df_popularidad_pizza.values
plt.figure(figsize=(15,10))
sns.barplot(x=x, y=y.flatten(),palette="mako")
plt.xticks(rotation = 45)
plt.savefig('grafico2.png', bbox_inches = 'tight')
pdf.image('grafico2.png', x = 8, w = 190)
pdf.ln()
pdf.ln()
pdf.set_font('helvetica', '', 10)
pdf.multi_cell(0, 10, txt = 'Del gráfico de barras superior podemos sacar las siguientes conclusiones:\nTop 3 pizzas más vendidas:                      Top 3 pizzas menos vendidas:')
pdf.ln(8)
pdf.multi_cell(0, 10, txt = '   1. Classic Dlx                                              1. Brie Carre\n   2. Hawaiian                                                 2. Spinach Supreme\n   3. BBQ Chicken                                          3. Mediterraneo')
pdf.ln()
#siguiente página
#utilizo un pie chart para mostrar las top 10 pizzas más populares de Maven Pizza
pdf.add_page()
pdf.set_font('helvetica', 'B', 12)
pdf.multi_cell(0, 10, txt = 'MAVEN PIZZA TOP 10', align = 'C')
pdf.ln()
#selecciono las 10 últimas filas del data frame df_popularidad_pizza que se corresponde con las 10 pizzas más populares
top10 = df_popularidad_pizza.tail(n= 10)
y = top10.values
mylabels = top10.index
plt.figure(figsize = (10,8))
plt.pie(y.flatten(), labels = mylabels, autopct= '%1.1f%%')
plt.savefig('piechart.png')
pdf.image('piechart.png', x = 20, y = 40, w = 170)
pdf.output('pdfpizza.pdf')

