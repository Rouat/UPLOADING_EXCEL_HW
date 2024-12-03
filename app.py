from flask import Flask, render_template, request, redirect, url_for, flash
import random
import pandas as pd
from genetic_algorithm import genetic_algorithm, Driver

app = Flask(__name__)
app.secret_key = 'secret_key'

drivers = []
about1 = [
    {
        'name': ' أنس أبو بكر',
        'icon': '2.png',
        'id': 'Anas_173490 '
    }, 
    {
        'name': 'محمد حازم دياب',
        'icon': '2.png',
        'id': 'Mohammed_Hazem_156460'
    },
    {
        'name': 'محمد عيسى',
        'icon': '2.png',
        'id': 'mohamed_153370'
    },

    {
        'name': 'تيماء البوش',
        'icon': '2.png',
        'id': 'taima_163087'
    },

        {
        'name': 'روئا حيلاني',
        'icon': '2.png',
        'id': 'roaa_146640'
    },

        {
        'name': 'أميرة النعسان',
        'icon': '2.png',
        'id': 'amera_153818'
    },

        {
        'name': 'باسل الحبيب',
        'icon': '2.png',
        'id': 'basl_113027 '
    },

]
@app.route('/')
def home():
    return render_template('index.html',about1=about1)

@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        name = request.form['name']
        cost = float(request.form['cost'])
        quality = int(request.form['quality'])
        capacity = int(request.form['capacity'])
        fuel_consumption = float(request.form['fuel_consumption'])
        reliability = int(request.form['reliability'])

        if name and cost and quality and capacity and fuel_consumption and reliability:
            driver = Driver(name, cost, quality, capacity, fuel_consumption, reliability)
            drivers.append(driver)
            flash('تمت إضافة السائق بنجاح!', 'success')
        else:
            flash('يرجى إدخال جميع البيانات بشكل صحيح!', 'danger')
        
        return redirect(url_for('add_driver'))
    return render_template('add_driver.html')

@app.route('/add_driver_excel', methods=['GET', 'POST'])
def add_driver_excel():
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            try:
                df = pd.read_excel(file)
                for _, row in df.iterrows():
                    driver = Driver(
                        name=row['name'],
                        cost=float(row['cost']),
                        quality=int(row['quality']),
                        capacity=int(row['capacity']),
                        fuel_consumption=float(row['fuel_consumption']),
                        reliability=int(row['reliability'])
                    )
                    drivers.append(driver)
                flash('تمت إضافة السائقين من الملف بنجاح!', 'success')
            except Exception as e:
                flash(f'حدث خطأ أثناء قراءة الملف: {e}', 'danger')
        else:
            flash('يرجى اختيار ملف Excel صحيح!', 'danger')

        return redirect(url_for('add_driver_excel'))

    return render_template('add_driver_excel.html')

@app.route('/generate_schedule')
def generate_schedule_view():
    if not drivers:
        flash('يرجى إضافة السائقين أولاً!', 'danger')
        return redirect(url_for('add_driver'))
    
    schedule = genetic_algorithm(drivers)
    return render_template('schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
