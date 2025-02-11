


<%--<%@ page contentType="text/html" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="styleF.css">
        <title>Faculty Login</title>
    </head>
    <body>
        <div class="container">
            <h1>Faculty Login</h1>
            <form action="FacultyLogin" method="post">
                <label for="faculty_id">Faculty ID:</label>
                <input type="text" id="faculty_id" name="faculty_id" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Login</button>
            </form>

            <p><a href="index.html">Back to Home</a></p>

            <!-- Display error message if present -->
            <% 
                String errorMessage = (String) session.getAttribute("errorMessage");
                if (errorMessage != null) {
            %>
                <p style="color: red;"><%= errorMessage %></p>
                <% session.removeAttribute("errorMessage"); %>
            <% } %>
        </div>
    </body>
</html>
--%>
<%@ page contentType="text/html" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="styleF.css">
        <title>Faculty Login</title>
    </head>
    <body>
        <div class="container">
            <h1>Faculty Login</h1>
            <!-- Add autocomplete="off" to the form -->
            <form action="FacultyLogin" method="post" autocomplete="off">
                <label for="faculty_id">Faculty ID:</label>
                <input type="text" id="faculty_id" name="faculty_id" value="" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" value="" required><br>
                <button type="submit">Login</button>
            </form>

            <p><a href="index.html">Back to Home</a></p>

            <!-- Display error message if present -->
            <% 
                String errorMessage = (String) session.getAttribute("errorMessage");
                if (errorMessage != null) {
            %>
                <p style="color: red;"><%= errorMessage %></p>
                <% 
                    session.removeAttribute("errorMessage"); 
                %>
            <% } %>
        </div>
    </body>
</html>
