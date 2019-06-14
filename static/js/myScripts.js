function renderIngredientElement(type, counter) {

    units = ["g", "mg", "kg", "ml", "l", "tsp", "tbsp", "cup", "glass", "whole", "half", "quater", "slice"]

    var options = ""

    units.forEach(function(unit) {
        options += `<option value="${unit}">${unit}</option>`
    });

    if (type === "li") {
        return `
        <li>
            <div class="form-row mb-1" id="ingredient${counter}">
              <div class="col-12 mb-1">
                <input type="text" class="form-control form-control-sm" id="ingredient${counter}_name" name="ingredient${counter}_name" required>
              </div>
              <div class="col-12 mb-1">
                <div class="input-group">
                  <input type="number" class="form-control form-control-sm" id="ingredient${counter}_amount" name="ingredient${counter}_amount" required>
                  <div class="input-group-append">
                    <select class="custom-select custom-select-sm btn" name="ingredient${counter}_unit" id="ingredient${counter}_unit">
                        ${options}
                    </select>
                  </div>
                </div>
              </div>
            </div>
         </li>`;
    }
    else if (type === "div") {
        return `
        <div class="form-row mb-1" id="ingredient${counter}">
          <div class="col-12 col-sm-6 form-group">
            <label for="ingredient${counter}_name">Ingredient<span class="d-none d-sm-inline">'s Name</span></label>
            <input type="text" class="form-control" id="ingredient${counter}_name" name="ingredient${counter}_name" required>
          </div>
          <div class="col-12 col-sm-6 form-group">
            <label class="d-none d-sm-block" for="ingredient${counter}_amount">Amount</label>
            <div class="input-group">
              <input type="number" class="form-control" id="ingredient${counter}_amount" name="ingredient${counter}_amount" required>
              <div class="input-group-append">
                <select class="custom-select btn" name="ingredient${counter}_unit" id="ingredient${counter}_unit">
                    ${options}
                </select>
              </div>
            </div>
          </div>
        </div>`;
    }
}

$('#btn-add-ingredient').click(function() {
    let counter = $('#ingredient-counter').attr('value');
    counter++;

    var html_newIngredient = renderIngredientElement($('#ingredient-list').is('ul') ? "li" : "div", counter);

    $(html_newIngredient).insertAfter(`#ingredient${counter - 1}`);

    $('#ingredient-counter').attr('value', `${counter}`);

})

$('#btn-add-step').click(function() {
    let counter = $('#steps-counter').attr('value');

    counter++;

    var html_newStep = `
        <div class="form-row" id="step${counter}">
          <div class="col-12 mb-2">
            <div class="input-group form-group">
              <div class="input-group-prepend">
                <label for="recipe_step_${counter}" class="input-group-text">Step ${counter}</label>
              </div>
              <textarea class="form-control" id="recipe_step_${counter}" name="recipe_step_${counter}" rows="1" required></textarea>
            </div>
          </div>
        </div>`;


    $(html_newStep).insertAfter(`#step${counter - 1}`);

    $('#steps-counter').attr('value', `${counter}`);
    //alert($('#ingredient-counter').attr('value'));

})

$('#btn-rm-ingredient').click(function() {
    let counter = $('#ingredient-counter').attr('value');
    if (counter > 1) {
        $(`#ingredient${counter}`).remove();

        counter--;
        $('#ingredient-counter').attr('value', `${counter}`);
    }
})

$('#btn-rm-step').click(function() {
    let counter = $('#steps-counter').attr('value');
    if (counter > 1) {
        $(`#step${counter}`).remove();

        counter--;
        $('#steps-counter').attr('value', `${counter}`);
    }
})


$('#rating_block').children('span').click(function() {


    if ($(this).attr('id') === "rate1") {
        colorSpoon("rate2", false);
        colorSpoon("rate3", false);
        colorSpoon("rate4", false);
        colorSpoon("rate5", false);
        $('#rating_counter').attr('value', 1);
    }
    else if ($(this).attr('id') === "rate2") {
        colorSpoon("rate2", true);
        colorSpoon("rate3", false);
        colorSpoon("rate4", false);
        colorSpoon("rate5", false);
        $('#rating_counter').attr('value', 2);
    }
    else if ($(this).attr('id') === "rate3") {
        colorSpoon("rate2", true);
        colorSpoon("rate3", true);
        colorSpoon("rate4", false);
        colorSpoon("rate5", false);
        $('#rating_counter').attr('value', 3);
    }
    else if ($(this).attr('id') === "rate4") {
        colorSpoon("rate2", true);
        colorSpoon("rate3", true);
        colorSpoon("rate4", true);
        colorSpoon("rate5", false);
        $('#rating_counter').attr('value', 4);
    }
    else if ($(this).attr('id') === "rate5") {
        colorSpoon("rate2", true);
        colorSpoon("rate3", true);
        colorSpoon("rate4", true);
        colorSpoon("rate5", true);
        $('#rating_counter').attr('value', 5);
    }

    // let x = 0;


    // if      ($(this).attr('id') === "rate1")   x = 1
    // else if ( $(this).attr('id') === "rate2")  x = 2
    // else if ( $(this).attr('id') === "rate3")  x = 3
    // else if ( $(this).attr('id') === "rate4")  x = 4
    // else if ( $(this).attr('id') === "rate5")  x = 5

    // for (var i = 1; i < x  i--; ) {

    // }

})

function colorSpoon(elementId, mode) {

    //$('#rating_block').children('span').removeClass("text-primary").removeClass("text-secondary")

    $(`#${elementId}`).removeClass("text-primary").removeClass("text-secondary")

    if (mode) {
        $(`#${elementId}`).addClass("text-primary")
    }
    else {
        $(`#${elementId}`).addClass("text-secondary")
    }
    return
}
