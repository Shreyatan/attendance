<%-- 
    Document   : AdminLogin
    Created on : Jan 22, 2025, 6:41:19 PM
    Author     : Lenovo
--%>


<%@ page contentType="text/html" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="styleA.css">
        <title>Admin Login</title>
    </head>
    <body>
        <div class="container">
            <h1>Admin Login</h1>
            <form action="AdminLogin" method="post">
                <label for="admin_id">Admin ID:</label>
                <input type="text" id="admin_id" name="admin_id" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
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
