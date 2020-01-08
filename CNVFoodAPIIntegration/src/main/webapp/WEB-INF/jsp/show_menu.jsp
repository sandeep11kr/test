<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>ConverseNow - Menu Details</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  <style>
  ul {
      padding: 0;
      list-style-type: none;
  }
  </style>
</head>
<body>
    <div class="container">
      <p><a href="/">Home</a></p>
      <div class="container">
       <p>
        <a href="/restaurant/excel?id=${id}" class="btn btn-success float-right">
          <span class="oi oi-data-transfer-download"></span> Download Report
        </a>
       </p>
      </div>
      <div class="container">
          <div class="table-responsive">
           <table class="table table-sm table-bordered">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Address</th>
                  <th>City</th>
                  <th>Postal Code</th>
                  <th>Ingredients API</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>${restaurant.restaurant_name}</td>
                  <td>${restaurant.address_1} ${restaurant.address_2}</td>
                  <td>${restaurant.city_town}</td>
                  <td>${restaurant.postal_code}</td>
                  <td>${api}</td>
                </tr>
              </tbody>
           </table>
          </div>
      </div>
    </div>
    <div class="container">
    <p class="text-danger">For the table below, scroll horizontally to see the complete details</p>
        <div class="table-responsive">
         <table class="table table-sm table-bordered">
            <thead>
                <th>Name</th>
                <th>Group</th>
                <th>Item Description</th>
                <th>Price</th>
                <th>Calories</th>
                <th>Heat Index</th>
                <th>Vegetarian</th>
                <th>Vegan</th>
                <th>Allergy Information</th>
                <th>Allergens</th>
                <th>Special</th>
                <th>Halal</th>
                <th>Kosher</th>
                <th>Gluten Free</th>
              </tr>
            </thead>
            <tbody>
                <c:forEach items="${restaurant.menus}" var="menu">
                <c:forEach items="${menu.menu_groups}" var="group">
                <c:forEach items="${group.menu_items}" var="item">
                  <tr>
                    <td><a href="/ingredients?name=${item.menu_item_name}&api=${api}">${item.menu_item_name}</a></td>
                    <td>${group.group_name}</td>
                    <td>${item.menu_item_description}</td>
                    <td>${item.menu_item_price}</td>
                    <td>${item.menu_item_calories}</td>
                    <td>${item.menu_item_heat_index}</td>
                    <td>${item.vegetarian}</td>
                    <td>${item.vegan}</td>
                    <td>${item.menu_item_allergy_information}</td>
                    <td>${item.menu_item_allergy_information_allergens}</td>
                    <td>${item.special}</td>
                    <td>${item.halal}</td>
                    <td>${item.kosher}</td>
                    <td>${item.gluten_free}</td>
                  </tr>
                </c:forEach>
                </c:forEach>
                </c:forEach>
            </tbody>
          </table>
        </div>
    </div>
</body>
</html>