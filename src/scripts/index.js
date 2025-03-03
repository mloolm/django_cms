import $ from "jquery";
import 'bootstrap';
import './theame_common/functions'

$(function (){
    //Donation form
    if($('#main_donation_form').is('#main_donation_form'))
    {
        function init_error(error)
        {
            console.error(error)

        }

        function setActive(target, val)
        {
            $('input[name='+target+']').val(val)

            $('#main_donation_form [data-action=switch][data-target='+target+'] [data-value]').removeClass('active')
            $('#main_donation_form [data-action=switch][data-target='+target+'] [data-value='+ val +']').addClass('active')
        }

        //Init form
        $('#main_donation_form [data-action=switch] .active').each(function (o,i){
            let def_val = $(this).attr('data-value');
            if((typeof def_val != 'string') || !def_val.length)
            {
                init_error('Error if form: bad default vals')
                return
            }

            let target = $($(this).parents('[data-action=switch]')[0]).attr('data-target')
            if((typeof target != 'string') || !target.length)
            {
                init_error('Error if form: bad data-target vals')
                return
            }

            $('input[name='+target+']').val(def_val)
        })

        $('#main_donation_form [data-action=switch] [data-value]').click(function (){
            let target = $($(this).parents('[data-action=switch]')[0]).attr('data-target')
            let val = $(this).attr('data-value')

            setActive(target, val)

            if(target == 'provider')
            {
                //Check donation types
                let dn = $(this).attr('data-donation-type').split(',')

                $('#main_donation_form [data-action=switch][data-target=donation_type] [data-value]').attr('disabled', 'disabled')
                for (let i in dn)
                {
                    $('#main_donation_form [data-action=switch][data-target=donation_type] [data-value='+dn[i]+']').removeAttr('disabled')
                }

                //if selected became disabled
                if($('#main_donation_form [data-action=switch][data-target=donation_type] [data-value][disabled].active').is('.active'))
                {
                    let new_val = $($('#main_donation_form [data-action="switch"][data-target="donation_type"] [data-value]:not(:disabled)')[0]).attr('data-value')
                    setActive('donation_type', new_val)
                }

                let provider_name =  $(this).attr('data-value')
                if(provider_name == 'crypto')
                {
                    $('[data-content=money]').addClass('d-none')
                    $('[data-content=crypto]').removeClass('d-none')
                }
                else
                {
                    $('[data-content=crypto]').addClass('d-none')
                    $('[data-content=money]').removeClass('d-none')

                }


            }

        })

        if($('#main_donation_form [data-action=copy_wallet]').is('[data-action]'))
        {
            $('#main_donation_form [data-action=copy_wallet]').click(function (){
            // Находим соответствующий input с данным data-wallet
            var walletId = $(this).data('target');
            var input = $('input[data-wallet="' + walletId + '"]');

            // Выбираем текст в input
            input.select();
            input[0].setSelectionRange(0, 99999); // Для мобильных устройств

            let btn = this;
            $(btn).addClass('copied')
            // Копируем текст в буфер обмена
            navigator.clipboard.writeText(input.val()).then(function() {
                setTimeout(function (){
                    $(btn).removeClass('copied')

                }, 2000)
            }).catch(function(err) {
                alert('Не удалось скопировать: ' + err);
            });
                });
            }



    }


     if($('.ext-icon[data-icon-url]').is('.ext-icon'))
        {

            $('.ext-icon[data-icon-url]').each(function (i,o){
                let url = $(o).attr('data-icon-url')
                let icon = o;

                fetch(url)
                    .then(response => response.text())
                    .then(svg => {
                    $(icon).html(svg)
                });
            });
        }
})