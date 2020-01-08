<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>ConverseNow - List Of Ingredients</title>
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
          <a href="/ingredients/excel?name=${name}" class="btn btn-success float-right">
            <span class="oi oi-data-transfer-download"></span> Download Report
          </a>
         </p>
         <p class="text-danger">For the table below, scroll horizontally to see the complete details</p>
          <div class="table-responsive">
           <table class="table table-sm table-bordered">
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Manufacturer</th>
                  <th>Food Group</th>
                  <th>Refuse Percentage</th>
                  <th>Refuse Description</th>
                  <th>Weight in grams</th>
                  <th>Measurements</th>
                  <th>Claims</th>
                  <th>Calories</th>
                  <th>Nutrition</th>
                </tr>
              </thead>
              <tbody>
                <c:forEach items="${ingredients}" var="ingredient">
                <tr>
                  <td>${ingredient.description}</td>
                  <td>${ingredient.manufacturer}</td>
                  <td>${ingredient.food_group}</td>
                  <td>${ingredient.refuse_percentage}</td>
                  <td>${ingredient.refuse_description}</td>
                  <td>${ingredient.weight_in_grams}</td>
                  <td>
                    <table>
                        <thead>
                            <th>Description</th>
                            <th>Weight Amount</th>
                            <th>Weight In Grams</th>
                            <th>Edible Portion</th>
                        </thead>
                        <tbody>
                            <c:forEach items="${ingredient.measurements}" var="measurement">
                                <tr>
                                    <td>${measurement.description}</td>
                                    <td>${measurement.weight_amount}</td>
                                    <td>${measurement.weight_grams}</td>
                                    <td>${measurement.edible_portion}</td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                  </td>
                  <td>
                    <table>
                        <thead>
                            <th>Alcohol Free</th>
                            <th>Sodium Free</th>
                            <th>Good Source Protein</th>
                            <th>High Protein</th>
                            <th>Good Source Fiber</th>
                            <th>High Fiber</th>
                        </thead>
                        <tbody>
                            <tr>
                                <td>${ingredient.claims.alcohol_free}</td>
                                <td>${ingredient.claims.sodium_free}</td>
                                <td>${ingredient.claims.good_source_protein}</td>
                                <td>${ingredient.claims.high_protein}</td>
                                <td>${ingredient.claims.good_source_fiber}</td>
                                <td>${ingredient.claims.high_fiber}</td>
                            </tr>
                        </tbody>
                    </table>
                  </td>
                  <td>
                    <table>
                        <thead>
                            <th>Calories Alcohol</th>
                            <th>Calories Fat</th>
                            <th>Calories Carbohydrates</th>
                            <th>Calories Protein</th>
                            <th>Total</th>
                        </thead>
                        <tbody>
                            <tr>
                                <td>${ingredient.calories.calories_alcohol}</td>
                                <td>${ingredient.calories.calories_fat}</td>
                                <td>${ingredient.calories.calories_carbohydrates}</td>
                                <td>${ingredient.calories.calories_protein}</td>
                                <td>${ingredient.calories.total}</td>
                            </tr>
                        </tbody>
                    </table>
                  </td>
                  <td>
                      <table>
                          <thead>
                              <th>Name</th>
                              <th>Amount</th>
                              <th>Units</th>
                              <th>Daily Percentage</th>
                          </thead>
                          <tbody>
                               <c:forEach items="${ingredient.nutritions}" var="nutrition">
                                  <tr>
                                      <td>${nutrition.name}</td>
                                      <td>${nutrition.amount}</td>
                                      <td>${nutrition.units}</td>
                                      <td>${nutrition.daily_value}</td>
                                  </tr>
                               </c:forEach>
                          </tbody>
                      </table>
                  </td>
                </tr>
                </c:forEach>
              </tbody>
           </table>
          </div>
      </div>
    </div>
</body>
</html>