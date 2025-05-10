from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  
from django.contrib import messages
from .models import Employee, Payslip


def employee_page(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employee_page.html', {'employee_objects': employee_objects})

def add_overtime(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        overtime_hours = float(request.POST.get('overtime_hours', 0))
        
        if overtime_hours < 0:
            messages.error(request, "Overtime hours cannot be negative.")
        else:
            overtime_pay = (employee.rate / 160) * 1.5 * overtime_hours
            employee.overtime_pay += overtime_pay
            employee.save()
        
        return redirect(reverse('payroll_app:employee_page'))
    else:
        return render(request, 'payroll_app/add_overtime.html', {'employee': employee})

def search(request):
    search_query = request.GET.get('search_query', '')
    employees = Employee.objects.filter(name__icontains=search_query) | Employee.objects.filter(id_number__icontains=search_query)
    return render(request, 'payroll_app/search_employee.html', {'employee_objects': employees, 'search_query': search_query})

def search_employee(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        employees = Employee.objects.filter(name__icontains=search_query) | Employee.objects.filter(id_number__icontains=search_query)
        if not employees:
            messages.info(request, "No such employee found.")
    else:
        employees = Employee.objects.all()
    return render(request, 'payroll_app/search_employee.html', {'employee_objects': employees, 'search_query': search_query})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method =='POST':
        button = request.POST.get('button')
        if button == 'Delete':
            employee.delete()
    return redirect(reverse('payroll_app:employee_page'))


def update_employee(request, employee_id):
    #This code is for the update employee button and page redirection to update_employee.html
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method =='POST':
        button = request.POST.get('button')
        if button == 'Update':
             return redirect(reverse('payroll_app:update_employee', kwargs={'employee_id':employee_id}))  
    return render(request, 'payroll_app/update_employee.html', {'employee': employee})

def updateEmployee_Page(request, employee_id):
    #Insert here code for the page on updating employee records/update_employee.html
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method =='POST':
        button = request.POST.get('button')
        if button == 'Update':
             return redirect(reverse('payroll_app:updateEmployee_page', kwargs={'employee_id':employee_id})) 
    return render(request, 'payroll_app/update_employee.html', {'employee': employee})



def update_record(request, employee_id):
    if request.method == 'POST':
        j = request.POST.get('name', '')
        # g = request.POST.get('id_number', '')
        o = request.POST.get('rate', '')
        a = request.POST.get('allowance', None)
        
        # Get the current employee
        employee = get_object_or_404(Employee, id=employee_id)
        
        if not j or not o:
            error_message = "All fields are required!"
            return render(request, 'payroll_app/update_employee.html', {'employee': employee, 'error_message': error_message})

        try:
            # g = int(g)
            o = float(o)
            if a is not None and a.strip() != "":
                a = float(a)
            else:
                a = float(0)
            
            if o < 0 or (a is not None and a < 0):
                error_message = "ID Number, rate, and allowance cannot be negative!"
                return render(request, 'payroll_app/update_employee.html', {'employee': employee, 'error_message': error_message})
        except ValueError:
            error_message = "ID Number, rate, and allowance must be valid numbers!"
            return render(request, 'payroll_app/update_employee.html', {'employee': employee, 'error_message': error_message})
        
        # Get the payslips associated with the old ID number
        old_payslips = Payslip.objects.filter(id_number=employee)
        
        # Delete payslips associated with the old ID number
        old_payslips.delete()

        # Calculate new overtime pay based on updated rate
        employee.name = j
        employee.rate = o
        employee.allowance = a
        employee.save()

        return redirect(reverse('payroll_app:employee_page'))
    else:
        employee = Employee.objects.get(id=employee_id)
        return render(request, 'payroll_app/update_employee.html', {'employee': employee})




def create_employee(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        overtime_pay = 0
        
        # If Allowance field is empty
        if not allowance:
            allowance = 0

        # Check if all required fields are provided
        if not name or not id_number or not rate:
            error_message = "Name, ID Number, and Rate are required fields!"
            return render(request, 'payroll_app/create_employee.html', {'error_message': error_message})

        # Invalid. Employee ID Number has been recorded already.
        if Employee.objects.filter(id_number=id_number).exists():
            error_message = "Invalid. ID Number has been recorded already."
            return render(request, 'payroll_app/create_employee.html', {'error_message': error_message})

        # Check if ID Number and Rate are valid numbers
        try:
            id_number = int(id_number)
            rate = float(rate)
            allowance = float(allowance)

        except ValueError:
            error_message = "ID Number, Rate, and Allowance must be valid numbers!"
            return render(request, 'payroll_app/create_employee.html', {'error_message': error_message})

        # Check for negative numbers
        if int(id_number) < 0 or float(rate) < 0 or float(allowance) < 0:
            error_message = "ID Number, rate, and allowance cannot be negative!"
            return render(request, 'payroll_app/create_employee.html', {'error_message': error_message})
        
        # Create the Employee object
        employee = Employee.objects.create(
            name=name,
            id_number=id_number,
            rate=rate,
            allowance=allowance,
            overtime_pay = overtime_pay
        )
        
        # Redirect to the employee page
        return redirect('payroll_app:employee_page')
    else:
        return render(request, 'payroll_app/create_employee.html')


def payslips_page(request):
    all_employee_ids = Employee.objects.values_list('id_number', flat=True)
    # initialize id number variable
    id_number = None
    # initialize year variable
    year = None

    # Initialize payslips_summary as an empty list
    payslips_summary = []

    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        year = request.POST.get('year')
        month = request.POST.get('month')
        cycle = request.POST.get('cycle')

        # checks if all fields are filled out
        if not id_number or not month or not cycle or not year:
            error_message = "Invalid. All fields are required!"
            employees = Employee.objects.all()
            return render(request, 'payroll_app/payslips_page.html', {'error_message': error_message, 'employees': employees, 'all_employee_ids': all_employee_ids})
        # for duplicates
    
        # checks if year is a number
        if not year.isdigit():
            error_message = "Invalid. Year must be a valid number!"
            employees = Employee.objects.all()
            return render(request, 'payroll_app/payslips_page.html', {'error_message': error_message, 'employees': employees})
        
        # checks if year is negative
        if int(year) < 0:
            error_message = "Invalid. Year cannot be negative!"
            employees = Employee.objects.all()
            return render(request, 'payroll_app/payslips_page.html', {'error_message': error_message, 'employees': employees})
        
        # checks if employees exists, filters employees & resolves error of "field id expected a number but got 'all employees'"
        if id_number == 'All Employees':
            employees = Employee.objects.all()
        else:
            try:
                # Try converting id_number to int and then filter
                id_number = int(id_number)
                employees = Employee.objects.filter(id_number=id_number)
            except ValueError:
                error_message = "Invalid. Employee does not exist!"
                employees = Employee.objects.all()
                return render(request, 'payroll_app/payslips_page.html', {'error_message': error_message, 'employees': employees, 'all_employee_ids': all_employee_ids})

        request.session['selected_id_number'] = id_number
        for employee in employees:
            # Check if payslips already exist for this employee, month, year, and cycle
            existing_payslips = Payslip.objects.filter(
                id_number=employee,
                year=year,
                month=month,
                pay_cycle=cycle
            )

            # If payslip already exists for this employee, month, year, and cycle, show an error message and continue with the next employee
            
            '''
            if existing_payslips.exists():
                error_message = f"A payslip for employee {employee.id_number} already exists for the selected month, year, and cycle."
                employees = Employee.objects.all()
                return render(request, 'payroll_app/payslips_page.html', {'error_message': error_message, 'employees': employees, 'all_employee_ids': all_employee_ids})
            '''
            
            if existing_payslips.exists():
                messages.error(request, f"A payslip for employee {employee.id_number} already exists for the selected month, year, and cycle.")
                # error_message = f"A payslip for employee {employee.id_number} already exists for the selected month, year, and cycle."
                # messages.error(request, error_message)
                continue
            
            if cycle == '1':
                date = '1-15'
                pag_ibig = 100
                tax = ((employee.rate/2 + employee.allowance + employee.overtime_pay - pag_ibig) * 0.2)
                total_pay = ((employee.rate/2 + employee.allowance + employee.overtime_pay) - tax)
                deductions_health = 0
                sss = 0
            elif cycle == '2':
                date  = '16-30'
                deductions_health = employee.rate * 0.04
                sss = employee.rate * 0.045
                tax = ((employee.rate/2 + employee.allowance + employee.overtime_pay - deductions_health - sss) * 0.2)
                total_pay = ((employee.rate/2 + employee.allowance + employee.overtime_pay - deductions_health - sss) - tax)

            # create payslip object and save
            payslip = Payslip.objects.create(
                id_number=employee,
                month=month,
                year=year,
                pay_cycle=cycle,
                rate=employee.rate,
                earnings_allowance=employee.allowance,
                date_range=date,
                total_pay=total_pay,
                deductions_health=deductions_health,
                deductions_tax=tax,
                pag_ibig=pag_ibig if cycle == '1' else 0,
                sss=sss if cycle == '2' else 0,
                overtime=employee.overtime_pay
            )

            employee.overtime_pay = 0
            employee.save()
            
            # Append payslip data to the existing payslips_summary
            payslips_summary.append({
                'id': payslip.pk,
                'id_number': employee.id_number,
                'date': date,
                'month': month,
                'year': year,
                'cycle': cycle,
                'total_pay': total_pay,
                'deductions_health': deductions_health,
                'tax': tax
            })
            
        # Append new payslip data to existing payslips_summary
        request.session.setdefault('payslips_summary', []).extend(payslips_summary)
        request.session['selected_id_number'] = id_number
        request.session['selected_year'] = year

    if 'payslips_summary' in request.session:
        payslips_summary = []
        for payslip_data in request.session['payslips_summary']:
            # Check if payslip still exists
            if Payslip.objects.filter(pk=payslip_data.get('id', None)).exists():
                payslips_summary.append(payslip_data)
    if 'selected_id_number' in request.session:
        id_number = request.session['selected_id_number']
    if 'selected_year' in request.session:
        year = request.session['selected_year']

    employees = Employee.objects.all()


    return render(request, 'payroll_app/payslips_page.html', {
        'employees': employees,
        'payslips_summary': payslips_summary,
        'all_employee_ids': all_employee_ids,
        'selected_id_number': id_number if id_number else '',
        'year': year
    })

    

def view_payslips(request, id_number, year, month, cycle):
    try:
        # Convert cycle and year to integers for comparison
        cycle = int(cycle)
        year = int(year) 

        # Retrieve the employee object with the given id_number
        employee = Employee.objects.get(id_number=id_number)

        # Filter payslips based on employee, year, month, and cycle
        payslips = Payslip.objects.filter(id_number=employee, year=str(year), month=month, pay_cycle=cycle)
        
        # Get the payslip IDs, dates, month, and year for the selected payslips
        payslip_ids = payslips.values_list('pk', flat=True)
        payslip_dates = payslips.values_list('date_range', 'month', 'year')
        
        # Get the list of months and years for the payslips
        payslip_month = payslips.values_list('month', flat=True)
        payslip_year = payslips.values_list('year', flat=True)

        # If no payslips are found, display an error message
        if not payslips.exists():
            error_message = "No payslips found for the given parameters."
            return render(request, 'payroll_app/error_page.html', {'error_message': error_message})

        # Initialize an empty list to store payslip data
        payslip_list = []

        #initialize variables
        deductions_tax = 0.0
        pag_ibig = 0.0
        deductions_health = 0.0
        sss = 0.0
        rate = 0.0
        overtime_pay = 0.0
        allowance = 0.0

        # Iterate through each payslip and extract relevant data
        for payslip in payslips:
            if cycle == 1:
                rate = employee.rate
                overtime_pay = employee.overtime_pay
                allowance = employee.allowance
                gross_pay = rate + overtime_pay + allowance
                deductions_tax = payslip.deductions_tax
                pag_ibig = payslip.pag_ibig
                total_deductions = payslip.deductions_tax + payslip.pag_ibig
            elif cycle == 2:
                rate = employee.rate
                overtime_pay = employee.overtime_pay
                allowance = employee.allowance
                gross_pay = rate + overtime_pay + allowance
                deductions_tax = payslip.deductions_tax
                deductions_health = payslip.deductions_health
                sss = payslip.sss
                total_deductions = payslip.deductions_tax + payslip.deductions_health + payslip.sss

            # Calculate net pay for the payslip
            net_pay = ((employee.rate/2 + employee.allowance + employee.overtime_pay - deductions_health - sss) - deductions_tax)

            # Create a dictionary to store payslip data
            payslip_data = {
                'employee': employee,
                'payslip': payslip,
                'total_deductions': total_deductions,
                'net_pay': net_pay,
                'gross_pay': gross_pay,
                'payslip_id': payslip.pk,
                'payslip_dates': payslip.date_range,
                'payslip_month': payslip_month,  # Changed to a list of months
                'payslip_year': payslip_year,    # Changed to a list of years
                'cycle': cycle,
                'deductions_tax': deductions_tax,
                'pag_ibig': pag_ibig,
                'deductions_health': deductions_health,
                'sss': sss
            }

            # Append payslip data to the payslip_list
            payslip_list.append(payslip_data)

        # Render the view_payslips.html template with payslip data
        return render(request, 'payroll_app/view_payslips.html', {
            'payslip_list': payslip_list,
            'employee': employee,
            'payslip_ids': payslip_ids, 
            'payslip_dates': payslip_dates,
            'payslip_month': payslip_month,  # Passes the list of months to the template
            'payslip_year': payslip_year,    # Passes the list of years to the template
            'net_pay': net_pay,
            'total_deductions': total_deductions,
            'cycle': cycle,
            'deductions_tax': deductions_tax,
            'pag_ibig': pag_ibig,
            'deductions_health': deductions_health,
            'sss': sss
        })
    
    # Handle exceptions such as Employee.DoesNotExist and ValueError
    except (Employee.DoesNotExist, ValueError):
        error_message = "Error retrieving payslip details. Please check the parameters."
        return render(request, 'payroll_app/error_page.html', {'error_message': error_message})
    