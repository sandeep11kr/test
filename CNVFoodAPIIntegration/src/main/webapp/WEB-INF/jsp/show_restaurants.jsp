<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>ConverseNow - List Of Restaurants</title>
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
        <form action="/restaurant/search">
        <div class="row form-group">
          <div class="col-3">
              <label for="proxyUrl">Name:</label>
              <input type="text" class="form-control" id="name" name="name" value="${name}">
          </div>
          <div class="col-3">
              <label for="proxyUrl">Postal Code:</label>
              <input type="text" class="form-control" id="postal_code" name="postal_code" value="${postal_code}">
          </div>
          <div class="col-3">
                <label for="city">City In United States:</label>
                <input type="text" class="form-control" id="city" name="city" value="${city}">
          </div>
          <div class="col-3">
                <label for="api">Ingredients API:</label>
                <select class="form-control" name="api">
                    <option value="openmenu" ${api.equals('openmenu') ? 'selected':''}>Openmenu</option>
                    <option value="spoonacular" ${api.equals('spoonacular') ? 'selected':''}>Spoonacular</option>
                </select>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Start</button>
        </form>
      </div>
      <div class="container">
          <div class="table-responsive">
           <table class="table table-sm">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Address</th>
                  <th>Postal Code</th>
                </tr>
              </thead>
              <tbody>
                <c:forEach items="${restaurants}" var="restaurant">
                <tr>
                  <td><a href="/restaurant/details?id=${restaurant.id}&api=${api}">${restaurant.restaurant_name}</a></td>
                  <td>${restaurant.address_1}, ${restaurant.address_2} ${restaurant.city_town}, ${restaurant.state_province}</td>
                  <td>${restaurant.postal_code}</td>
                </tr>
                </c:forEach>
              </tbody>
           </table>
          </div>
      </div>
    </div>
</body>
</html>