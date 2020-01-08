package com.conversenow.foodapi.ui

import com.conversenow.foodapi.openmenu.ExcelGenerator
import com.conversenow.foodapi.openmenu.Log
import com.conversenow.foodapi.openmenu.services.OpenMenuIngredientServices
import com.conversenow.foodapi.openmenu.services.OpenMenuMenuServices
import com.conversenow.foodapi.openmenu.services.OpenMenuRestaurantServices
import com.conversenow.foodapi.spoonacular.services.SpoonacularIngredientServices
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpEntity
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.stereotype.Controller
import org.springframework.ui.ModelMap
import org.springframework.web.bind.annotation.*

@Controller
@RequestMapping('')
class MenuView {
    @Autowired OpenMenuRestaurantServices omRestaurantServices
    @Autowired OpenMenuMenuServices omMenuServices
    @Autowired OpenMenuIngredientServices omIngredientServices
    @Autowired SpoonacularIngredientServices spoonacularIngredientServices
    @Autowired Log log
    @Autowired ExcelGenerator excelGenerator

    @ExceptionHandler(value = Exception.class)
    String defaultExceptionHandler(Exception e) {
        e.printStackTrace()
        'error'
    }
    @RequestMapping(value = '/restaurant/search', method = RequestMethod.GET)
    String showRestaurants(ModelMap model,  @RequestParam(name = "name", required = false) String name,
                    @RequestParam(name = "postal_code", required = false) String postalCode,
                            @RequestParam(name = "city", required = false) String city,
                           @RequestParam(name = "api", required = false) String api) {
        def restaurants = []
        if(city!=null || postalCode !=null)
            restaurants = this.omRestaurantServices.loadAtLocation(name, postalCode, city)
        model.put("postal_code", postalCode)
        model.put("city", city)
        model.put("name", name)
        model.put("api", api)
        model.put("restaurants", restaurants)
        return "show_restaurants"
    }
    @RequestMapping('/')
    String listReports(ModelMap model){
        return "show_restaurants"
    }
    @RequestMapping('/restaurant/details')
    String showDetails(ModelMap model, @RequestParam(name = "id", required = true) String id,
                       @RequestParam(name = "api", required = true) String api){
        def restaurantDetails = this.omMenuServices.loadRestaurantMenu(id)
        model.put('restaurant', restaurantDetails)
        model.put('id', id)
        model.put('api', api)
        return "show_menu"
    }
    @RequestMapping('/restaurant/excel')
    def @ResponseBody HttpEntity<byte[]> loadRestaurantMenuExcel(ModelMap model, @RequestParam(name = "id", required = true) String id){
        def restaurantDetails = this.omMenuServices.loadRestaurantMenu(id)
        File excelFile = this.excelGenerator.generateRestaurantReport(restaurantDetails)
        def excelContent = excelFile.readBytes()
        HttpHeaders header = new HttpHeaders();
        header.setContentType(new MediaType("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
        header.set(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=${excelFile.name}");
        header.setContentLength(excelContent.length);
        return new HttpEntity<byte[]>(excelContent, header);
    }

    @RequestMapping('/ingredients')
    String loadIngredients(ModelMap model, @RequestParam(name = "name", required = true) String name,
                           @RequestParam(name = "api", required = false) String api){
        def ingredients = null
        if(api=='openmenu')
            ingredients = this.omIngredientServices.loadIngredientDetails(name)
        else
            ingredients = this.spoonacularIngredientServices.loadIngredientDetails(name)
        model.put('ingredients', ingredients)
        model.put('name', name)
        return "show_ingredients"
    }
    @RequestMapping('/ingredients/excel')
    def @ResponseBody HttpEntity<byte[]> loadIngredientsExcel(ModelMap model, @RequestParam(name = "name", required = true) String name){
        def ingredients = this.omIngredientServices.loadIngredientDetails(name)
        File excelFile = this.excelGenerator.generateIngredientsReport(name, ingredients)
        def excelContent = excelFile.readBytes()
        HttpHeaders header = new HttpHeaders();
        header.setContentType(new MediaType("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
        header.set(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=${excelFile.name}");
        header.setContentLength(excelContent.length);
        return new HttpEntity<byte[]>(excelContent, header);
    }
}
