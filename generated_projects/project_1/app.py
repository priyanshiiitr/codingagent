

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    # Get form values, provide defaults for GET request
    num1_in = request.form.get('num1', '')
    num2_in = request.form.get('num2', '')
    operator_in = request.form.get('operator', '+')

    if request.method == 'POST':
        try:
            num1 = float(num1_in)
            num2 = float(num2_in)

            if operator_in == '+':
                result = num1 + num2
            elif operator_in == '-':
                result = num1 - num2
            elif operator_in == '*':
                result = num1 * num2
            elif operator_in == '/':
                if num2 == 0:
                    error = "Error: Division by zero is not allowed."
                else:
                    result = num1 / num2
            else:
                error = "Invalid operator."

        except ValueError:
            error = "Invalid input. Please enter numeric values."

    return render_template(
        'index.html',
        result=result,
        error=error,
        num1=num1_in,
        num2=num2_in,
        operator=operator_in
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

