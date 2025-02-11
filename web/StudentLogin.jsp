<%-- 
    Document   : StudentLogin
    Created on : Jan 22, 2025, 6:40:58 PM
    Author     : Lenovo
--%>

<%--<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/CSS" href="styleS.css">
        <title>JSP Page</title>
    </head>
    <body>
        <div class="container">
            <h1>Login</h1>
            <form action="StudentLogin" method="post"> <!-- Change method to "post" -->
                <label for="username">Student Id:</label>
                <input type="text" id="username" name="username" required><br>
                <button type="submit">Login</button>
            </form>

            <p><a href="index.html">Back to Home</a></p>

            
            <% String error = request.getParameter("error");
                if (error != null && error.equals("1")) { %>
                    <p style="color: red;">Invalid username or password. Please try again.</p>
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
        <link rel="stylesheet" type="text/css" href="styleS.css">
        <title>Student Login</title>
    </head>
    <body>
        <div class="container">
            <h1>Student Login</h1>
            <form action="StudentLogin" method="post">
                <label for="student_id">Student ID:</label>
                <input type="text" id="student_id" name="student_id" required><br>
                <button type="submit">Login</button>
            </form>

            <p><a href="index.html">Back to Home</a></p>

            <!-- Display error message if login fails -->
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
