$(document).ready(function(){
    $('.modal').modal();
});

$('.chips-autocomplete').chips({
  placeholder: 'Digite uma tag',
  secondaryPlaceholder: '+Tag',
  autocompleteOptions: {
    data: {
      'Família': null,
      'Amigo': null,
      'Trabalho': null,
      'Outro': null
    },
    limit: Infinity,
    minLength: 1
  }
});

$(document).ready(function(){
  $('#btnClear').click(function(){
    if(confirm("Deseja mesmo limpar?")){
      /*Clear all input type="text" box*/
      $('#form1 input[type="text"]').val('')
      $('#form1 input[type="tel"]').val('')
      $(".chips .chip").remove();
      return false
    }
  });
});

function lerTags(){
  let instance = M.Chips.getInstance(document.getElementById("chip1"));
  let tags = ''
  
  instance.chipsData.forEach(element => {    
    if (tags == ''){
      tags = element.tag 
    }
    else{
      tags += ',' + element.tag
    }
  });
  $('#tags').val(tags)
}
function novoContato(){
  $('#salvar').html('SALVAR CONTATO<i class="material-icons right">add</i>')
  $('#tipo').val('novo')
}

function editarContato(id,nome,email,celular,tags){
  $('#salvar').html('SALVAR EDIÇÃO<i class="material-icons right">create</i>')
  $('#tipo').val('editar')
  $('#nome').val(nome)
  $('#email').val(email)
  $('#celular').val(celular)
  $('#id').val(id)

  let tagsl = tags.split(',')
  let instance = M.Chips.getInstance(document.getElementById("chip1"));
  tagsl.forEach(element => {
    instance.addChip({
      tag: element
    })
  })
}

