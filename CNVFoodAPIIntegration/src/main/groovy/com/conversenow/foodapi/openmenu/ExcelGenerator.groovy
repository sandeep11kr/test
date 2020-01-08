package com.conversenow.foodapi.openmenu
// https://mvnrepository.com/artifact/net.sourceforge.jexcelapi/jxl

import org.jxls.common.Context
import org.jxls.transform.Transformer
import org.jxls.util.JxlsHelper
import org.springframework.stereotype.Service

import javax.annotation.PostConstruct

@Service
class ExcelGenerator {
    def restaurantTemplateFile = null
    def ingredientTemplateFile = null
    @PostConstruct
    def init(){
        restaurantTemplateFile = new File(ExcelGenerator.class.getResource("/report").path, "restaurant_info.xlsx")
        ingredientTemplateFile = new File(ExcelGenerator.class.getResource("/report").path, "ingredient_info.xlsx")
    }
    def generateRestaurantReport(Restaurant restaurantObject){
        InputStream is = new FileInputStream(restaurantTemplateFile)
        File result = new File(ExcelGenerator.class.getResource("/report").path,
                "${restaurantObject.restaurant_name}_${restaurantObject.city_town}_${restaurantObject.postal_code}.xlsx")
        OutputStream os = new FileOutputStream(result)
        Context context = new Context();
        context.putVar("restaurant", restaurantObject)
        JxlsHelper helper = JxlsHelper.getInstance();
        Transformer transformer = helper.createTransformer(is,os);
        helper.processTemplate(context, transformer);
        result
    }
    def generateIngredientsReport(source, ingredients){
        InputStream is = new FileInputStream(ingredientTemplateFile)
        File result = new File(ExcelGenerator.class.getResource("/report").path,
                "${source}.xlsx")
        OutputStream os = new FileOutputStream(result)
        Context context = new Context();
        context.putVar("name", source)
        context.putVar("ingredients", ingredients)
        JxlsHelper helper = JxlsHelper.getInstance();
        Transformer transformer = helper.createTransformer(is,os);
        helper.processTemplate(context, transformer);
        result
    }
}
