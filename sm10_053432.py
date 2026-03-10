from flask import Flask, request, render_template_string
import numpy as np

app = Flask(__name__)

# ================= HOME PAGE =================
@app.route("/")
def home():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Engineering Maths Solver</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{ background:white; animation:fade 1s; }
@keyframes fade{ from{opacity:0} to{opacity:1} }
.title{ font-size:40px; font-weight:bold; color:#0d6efd; }
.subtitle{ font-style:italic; color:gray; }
.card{ transition:0.3s; }
.card:hover{ transform:scale(1.05); }
</style>
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold fs-3">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-5 text-center">
<div class="title">Engineering Maths Solver</div>
<p class="subtitle">
"Numerical methods transform mathematical theory into real world solutions."
</p>

<h3 class="mt-5 mb-4">Select a Numerical Method</h3>
<div class="row justify-content-center">

<div class="col-md-3">
<div class="card shadow p-4 text-center">
<h5>Bisection Method</h5>
<a href="/bisection" class="btn btn-primary">Open</a>
</div>
</div>

<div class="col-md-3">
<div class="card shadow p-4 text-center">
<h5>Newton Raphson</h5>
<a href="/newton" class="btn btn-primary">Open</a>
</div>
</div>

<div class="col-md-3">
<div class="card shadow p-4 text-center">
<h5>Forward Interpolation</h5>
<a href="/forward" class="btn btn-primary">Open</a>
</div>
</div>

<div class="col-md-3">
<div class="card shadow p-4 text-center">
<h5>Backward Interpolation</h5>
<a href="/backward" class="btn btn-primary">Open</a>
</div>
</div>

</div>
</div>
</body>
</html>
"""
    return render_template_string(html)

# ================= BISECTION METHOD =================
@app.route("/bisection", methods=["GET", "POST"])
def bisection():
    root = None
    error = None
    rows = []
    fx = ""

    if request.method == "POST":
        fx = request.form["fx"]
        a = float(request.form["a"])
        b = float(request.form["b"])
        tol = float(request.form["tol"])

        def f(x):
            return eval(fx)

        prev = None
        i = 1

        while True:
            c = (a + b) / 2
            if prev != None:
                error = abs((c - prev) / c) * 100
            else:
                error = 0

            rows.append([i, a, b, c, error])

            if prev != None and abs(c - prev) < tol:
                root = c
                break

            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
            prev = c
            i += 1

    html = """
<!DOCTYPE html>
<html>
<head>
<title>Bisection Method</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<h2 class="text-center mb-4">Bisection Method</h2>

<form method="POST" class="card p-4 shadow">
<label>Enter f(x)</label>
<input name="fx" class="form-control" required><br>
<label>a</label>
<input name="a" class="form-control" required><br>
<label>b</label>
<input name="b" class="form-control" required><br>
<label>Tolerance</label>
<input name="tol" class="form-control" required><br>
<button class="btn btn-primary">Calculate Root</button>
</form>

{% if root %}
<div class="card mt-4 p-3 shadow" style="font-family:'Courier New', monospace;">
<h4>Root = {{root}}</h4>
<h5 style="color:red;">Error Percentage = {{error}}</h5>
<form action="/graph" method="POST">
<input type="hidden" name="fx" value="{{fx}}">
<button class="btn btn-success mt-2">View Graph</button>
</form>
<a href="/bisection_info" class="btn btn-info mt-2">Method Details</a>

<table class="table table-bordered text-center mt-3">
<tr class="table-primary"><th>Iteration</th><th>a</th><th>b</th><th>c</th><th>Error %</th></tr>
{% for r in rows %}
<tr>
<td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td><td>{{r[4]}}</td>
</tr>
{% endfor %}
</table>
</div>
{% endif %}

</div>
</body>
</html>
"""
    return render_template_string(html, root=root, error=error, rows=rows, fx=fx)
# ================= BISECTION METHOD DETAILS =================
@app.route("/bisection_info")
def bisection_info():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Bisection Method Details</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<div class="card shadow p-4">
<h2 class="text-primary">Bisection Method</h2>
<h4 class="mt-3">Concept</h4>
<p>The Bisection Method is a numerical method to find roots of a function. It repeatedly halves an interval and selects the subinterval where the function changes sign.</p>
<h4>Formula</h4>
<p class="bg-light p-2">c = (a + b)/2</p>
<h4>Steps</h4>
<ol>
<li>Choose initial interval [a, b] such that f(a)*f(b) &lt; 0.</li>
<li>Compute midpoint c = (a + b)/2.</li>
<li>Check if f(a)*f(c) &lt; 0, set b = c, else a = c.</li>
<li>Repeat until |c_prev - c| &lt; tolerance.</li>
</ol>
</div>
</div>
</body>
</html>
"""
    return render_template_string(html)
# ================= NEWTON RAPHSON =================
from math import sin, cos, tan, exp, log, sqrt, pi

@app.route("/newton", methods=["GET", "POST"])
def newton():
    root = None
    rows = []
    error = None
    fx = ""

    # Safe dictionary for eval
    safe_dict = {"sin": sin, "cos": cos, "tan": tan, "exp": exp, 
                 "log": log, "sqrt": sqrt, "pi": pi}

    if request.method == "POST":
        fx = request.form["fx"]
        dfx = request.form["dfx"]
        x = float(request.form["x0"])
        tol = float(request.form["tol"])

        i = 1
        while True:
            # Evaluate function and derivative safely
            try:
                safe_dict["x"] = x
                f_val = eval(fx, {}, safe_dict)
                df_val = eval(dfx, {}, safe_dict)
            except Exception as e:
                root = f"Error in function evaluation: {e}"
                break

            if df_val == 0:
                root = "Derivative became zero. Cannot continue."
                break

            x1 = x - f_val / df_val
            error = abs((x1 - x) / x1) * 100 if x1 != 0 else 0
            rows.append([i, x, x1, error])

            if abs(x1 - x) < tol:
                root = x1
                break

            x = x1
            i += 1

    html = """
<!DOCTYPE html>
<html>
<head>
<title>Newton Raphson</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<h2 class="text-center">Newton Raphson Method</h2>

<form method="POST" class="card p-4 shadow">
<label>f(x)</label>
<input name="fx" class="form-control" required><br>
<label>f'(x)</label>
<input name="dfx" class="form-control" required><br>
<label>Initial Guess</label>
<input name="x0" class="form-control" required><br>
<label>Tolerance</label>
<input name="tol" class="form-control" required><br>
<button class="btn btn-primary">Calculate</button>
</form>

{% if root %}
<div class="card mt-4 p-3 shadow" style="font-family:'Courier New', monospace;">
<h4>Root = {{root}}</h4>
<h5 style="color:red;">Error = {{error}} %</h5>
<form action="/graph" method="POST">
<input type="hidden" name="fx" value="{{fx}}">
<button class="btn btn-success mt-2">View Graph</button>
</form>
<a href="/newton_info" class="btn btn-info mt-2">Method Details</a>

<table class="table table-bordered text-center mt-3">
<tr class="table-primary"><th>Iteration</th><th>x</th><th>x1</th><th>Error %</th></tr>
{% for r in rows %}
<tr>
<td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td>
</tr>
{% endfor %}
</table>
</div>
{% endif %}

</div>
</body>
</html>
"""
    return render_template_string(html, root=root, rows=rows, error=error, fx=fx)

# ================= NEWTON RAPHSON METHOD DETAILS =================
@app.route("/newton_info")
def newton_info():
    html = """
<!DOCTYPE html>
<html>

<head>
<title>Newton Raphson Method Details</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>

<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">

<div class="card shadow p-4">

<h2 class="text-primary">Newton-Raphson Method</h2>

<h4 class="mt-3">Concept</h4>
<p>
The Newton-Raphson Method is an iterative numerical technique to find roots of a function.
It starts with an initial guess and refines it using the function and its derivative.
</p>

<h4>Formula</h4>
<p class="bg-light p-2">
x<sub>n+1</sub> = x<sub>n</sub> - f(x<sub>n</sub>) / f'(x<sub>n</sub>)
</p>

<h4>Steps</h4>
<ol>
<li>Choose an initial guess x<sub>0</sub>.</li>
<li>Compute the next approximation: x<sub>n+1</sub> = x<sub>n</sub> - f(x<sub>n</sub>)/f'(x<sub>n</sub>).</li>
<li>Calculate the error = |x<sub>n+1</sub> - x<sub>n</sub>|.</li>
<li>Check if error &lt; tolerance. If yes, stop; else, set x<sub>n</sub> = x<sub>n+1</sub> and repeat step 2.</li>
</ol>

</div>

</div>

</body>
</html>
"""
    return render_template_string(html)

# ================= NEWTON FORWARD INTERPOLATION WITH GRAPH =================
@app.route("/forward", methods=["GET", "POST"])
def forward():
    rows = []
    result = None
    x_val = None
    x_points = []
    y_points = []

    if request.method == "POST":
        x_points = list(map(float, request.form["x_points"].split(',')))
        y_points = list(map(float, request.form["y_points"].split(',')))
        x_val = float(request.form["x_val"])

        n = len(x_points)
        diff_table = [y_points.copy()]
        for i in range(1, n):
            col = []
            for j in range(n - i):
                col.append(diff_table[i-1][j+1] - diff_table[i-1][j])
            diff_table.append(col)

        # Newton Forward formula
        h = x_points[1] - x_points[0]
        p = (x_val - x_points[0]) / h
        result = diff_table[0][0]
        p_prod = 1
        for i in range(1, n):
            p_prod *= (p - (i-1))
            result += (p_prod * diff_table[i][0]) / np.math.factorial(i)

        # Prepare table for frontend
        for i in range(n):
            row = [x_points[i], y_points[i]]
            for j in range(n - i):
                row.append(diff_table[j][i] if j <= len(diff_table[j])-1 else '')
            rows.append(row)

    html = """
<!DOCTYPE html>
<html>
<head>
<title>Newton Forward Interpolation</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<h2 class="text-center">Newton Forward Interpolation</h2>

<form method="POST" class="card p-4 shadow">
<label>X values (comma separated)</label>
<input name="x_points" class="form-control" required><br>
<label>Y values (comma separated)</label>
<input name="y_points" class="form-control" required><br>
<label>Value to interpolate</label>
<input name="x_val" class="form-control" required><br>
<button class="btn btn-primary">Calculate</button>
</form>

{% if result != None %}
<div class="card mt-4 p-3 shadow" style="font-family:'Courier New', monospace;">
<h4>Interpolated Value at x = {{x_val}} : {{result}}</h4>

<canvas id="chart"></canvas>

<a href="/forward_info" class="btn btn-info mt-2">Method Details</a>

<table class="table table-bordered text-center mt-3">
<tr class="table-primary"><th>X</th><th>Y</th>{% for i in range(1, rows|length) %}<th>Δ{{i}}</th>{% endfor %}</tr>
{% for row in rows %}
<tr>{% for val in row %}<td>{{val}}</td>{% endfor %}</tr>
{% endfor %}
</table>
</div>

<script>
let x_points = {{x_points}};
let y_points = {{y_points}};
let interp_x = {{x_val}};
let interp_y = {{result}};

new Chart(document.getElementById("chart"), {
    type: 'line',
    data: {
        labels: x_points,
        datasets: [
            {label: 'Data Points', data: y_points, borderWidth:2, borderColor:'blue', fill:false, tension:0.1},
            {label:'Interpolated Point', data: x_points.map(px => px === interp_x ? interp_y : null),
             borderColor:'red', backgroundColor:'red', pointRadius:5, showLine:false}
        ]
    },
    options: {
        scales: { y: { beginAtZero: true } }
    }
});
</script>

{% endif %}
</div>
</body>
</html>
"""
    return render_template_string(html, result=result, rows=rows, x_val=x_val, x_points=x_points, y_points=y_points)

# ================= NEWTON FORWARD METHOD DETAILS =================
@app.route("/forward_info")
def forward_info():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Newton Forward Interpolation Details</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<div class="card shadow p-4">
<h2 class="text-primary">Newton Forward Interpolation</h2>
<h4 class="mt-3">Concept</h4>
<p>
Newton Forward Interpolation is used to estimate the value of a function for a given
point based on equally spaced data points. It uses the forward difference table
and the formula derived from it.
</p>
<h4>Formula</h4>
<p class="bg-light p-2">
P(x) = y0 + pΔy0 + p(p-1)/2! Δ²y0 + ... + p(p-1)...(p-n+1)/n! Δⁿy0
</p>
<h4>Steps</h4>
<ol>
<li>Construct a forward difference table from the given data.</li>
<li>Compute p = (x - x0)/h where h = x1 - x0.</li>
<li>Apply Newton Forward formula to find interpolated value.</li>
<li>Repeat for other points if needed.</li>
</ol>
</div>
</div>
</body>
</html>
"""
    return render_template_string(html)

# ================= GRAPH =================
@app.route("/graph", methods=["POST"])
def graph():
    fx = request.form["fx"]
    x_vals = np.linspace(-10, 10, 100)
    if fx.strip() != "":
        y_vals = [eval(fx) for x in x_vals]
    else:
        y_vals = np.zeros_like(x_vals)
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Function Graph</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<h2 class="text-center">Function Graph</h2>
<canvas id="chart"></canvas>
</div>

<script>
let x={{x_vals}}
let y={{y_vals}}
new Chart(document.getElementById("chart"),{
type:"line",
data:{ labels:x, datasets:[{label:"f(x)", data:y, borderWidth:2}] }
})
</script>

</body>
</html>
"""
    return render_template_string(html, x_vals=list(x_vals), y_vals=y_vals)
# ================= NEWTON BACKWARD INTERPOLATION WITH GRAPH =================
@app.route("/backward", methods=["GET", "POST"])
def backward():
    rows = []
    result = None
    x_val = None
    x_points = []
    y_points = []

    if request.method == "POST":
        x_points = list(map(float, request.form["x_points"].split(',')))
        y_points = list(map(float, request.form["y_points"].split(',')))
        x_val = float(request.form["x_val"])

        n = len(x_points)
        diff_table = [y_points.copy()]
        for i in range(1, n):
            col = []
            for j in range(n - i):
                col.append(diff_table[i-1][j+1] - diff_table[i-1][j])
            diff_table.append(col)

        # Newton Backward formula
        h = x_points[1] - x_points[0]
        p = (x_val - x_points[-1]) / h
        result = diff_table[0][-1]
        p_prod = 1
        for i in range(1, n):
            p_prod *= (p + (i-1))
            result += (p_prod * diff_table[i][-1]) / np.math.factorial(i)

        # Prepare table for frontend
        for i in range(n):
            row = [x_points[i], y_points[i]]
            for j in range(n - i):
                row.append(diff_table[j][i] if j <= len(diff_table[j])-1 else '')
            rows.append(row)

    html = """
<!DOCTYPE html>
<html>
<head>
<title>Newton Backward Interpolation</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<h2 class="text-center">Newton Backward Interpolation</h2>

<form method="POST" class="card p-4 shadow">
<label>X values (comma separated)</label>
<input name="x_points" class="form-control" required><br>
<label>Y values (comma separated)</label>
<input name="y_points" class="form-control" required><br>
<label>Value to interpolate</label>
<input name="x_val" class="form-control" required><br>
<button class="btn btn-primary">Calculate</button>
</form>

{% if result != None %}
<div class="card mt-4 p-3 shadow" style="font-family:'Courier New', monospace;">
<h4>Interpolated Value at x = {{x_val}} : {{result}}</h4>

<canvas id="chart"></canvas>

<a href="/backward_info" class="btn btn-info mt-2">Method Details</a>

<table class="table table-bordered text-center mt-3">
<tr class="table-primary"><th>X</th><th>Y</th>{% for i in range(1, rows|length) %}<th>Δ{{i}}</th>{% endfor %}</tr>
{% for row in rows %}
<tr>{% for val in row %}<td>{{val}}</td>{% endfor %}</tr>
{% endfor %}
</table>
</div>

<script>
let x_points = {{x_points}};
let y_points = {{y_points}};
let interp_x = {{x_val}};
let interp_y = {{result}};

new Chart(document.getElementById("chart"), {
    type: 'line',
    data: {
        labels: x_points,
        datasets: [
            {label: 'Data Points', data: y_points, borderWidth:2, borderColor:'blue', fill:false, tension:0.1},
            {label:'Interpolated Point', data: x_points.map(px => px === interp_x ? interp_y : null),
             borderColor:'red', backgroundColor:'red', pointRadius:5, showLine:false}
        ]
    },
    options: {
        scales: { y: { beginAtZero: true } }
    }
});
</script>

{% endif %}
</div>
</body>
</html>
"""
    return render_template_string(html, result=result, rows=rows, x_val=x_val, x_points=x_points, y_points=y_points)


# ================= NEWTON BACKWARD METHOD DETAILS =================
@app.route("/backward_info")
def backward_info():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Newton Backward Interpolation Details</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand fw-bold" href="/">Engineering Maths Solver</a>
</div>
</nav>

<div class="container mt-4">
<div class="card shadow p-4">
<h2 class="text-primary">Newton Backward Interpolation</h2>
<h4 class="mt-3">Concept</h4>
<p>
Newton Backward Interpolation is used to estimate the value of a function for a given
point near the end of equally spaced data points. It uses the backward difference table
and the formula derived from it.
</p>
<h4>Formula</h4>
<p class="bg-light p-2">
P(x) = yn + pΔyn + p(p+1)/2! Δ²yn + ... + p(p+1)...(p+n-1)/n! Δⁿyn
</p>
<h4>Steps</h4>
<ol>
<li>Construct a backward difference table from the given data.</li>
<li>Compute p = (x - xn)/h where h = x1 - x0.</li>
<li>Apply Newton Backward formula to find interpolated value.</li>
<li>Repeat for other points if needed.</li>
</ol>
</div>
</div>
</body>
</html>
"""
    return render_template_string(html)
if __name__ == "__main__":
    app.run(debug=True)