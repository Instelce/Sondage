$('.topbar__toggle').click(function(e) {
    e.preventDefault();
    $('.topbar__nav').toggleClass('is-open');
    $('.toggle__icon').toggleClass('is-active');
})

const logo = document.querySelectorAll('#logo path');

for(let i = 0; i < logo.length; i++) {
    console.log(`Letter ${i} is ${logo[i].getTotalLength()}`);
}