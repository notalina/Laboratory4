'use strict';
(function () {
    $(document).ready(function () {
        $("#add_column_button").click(function(){
            let columns_count = $("#create_table_form .inputs .row").length
            let clone = $("#create_table_form .inputs .row").first().clone().appendTo("#create_table_form .inputs");
            $("#column_amount").attr("value", columns_count+1)
            $("#create_table_form .inputs .row").each(function( index ) {
                let column_name_input =  $(this).find("input").get(0); 
                let column_type_input =  $(this).find("input").get(1);
                $(column_name_input).attr("name", `column_types[${index}]`);
                $(column_type_input).attr("name", `column_types[${index}]`);
            });

        })
    })
}.call(this))