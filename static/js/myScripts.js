function renderIngredientElement(type, counter) {

    //units = ["g", "mg", "kg", "ml", "l", "tsp", "tbsp", "cup", "glass", "whole", "half", "quater", "slice"]

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
                        <option value="g">g</option>
                        <option value="mg">mg</option>
                        <option value="kg">kg</option>
                        <option value="ml">ml</option>
                        <option value="l">l</option>
                        <option value="tsp">tsp</option>
                        <option value="tbsp">tbsp</option>
                        <option value="cup">cup</option>
                        <option value="glass">glass</option>
                        <option value="whole">whole</option>
                        <option value="half">half</option>
                        <option value="quater">quater</option>
                        <option value="slice">slice</option>
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
                    <option value="g">g</option>
                    <option value="mg">mg</option>
                    <option value="kg">kg</option>
                    <option value="ml">ml</option>
                    <option value="l">l</option>
                    <option value="tsp">tsp</option>
                    <option value="tbsp">tbsp</option>
                    <option value="cup">cup</option>
                    <option value="glass">glass</option>
                    <option value="whole">whole</option>
                    <option value="half">half</option>
                    <option value="quater">quater</option>
                    <option value="slice">slice</option>
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

//function removeElement(prefix, start)
