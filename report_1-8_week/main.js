// const pageTurnBtn = document.querySelectorAll('.nextprev-btn back');

// pageTurnBtn.forEach((el, index) => {
//     el.onclick = () => {
//         const pageTurnId = el.getAttribute('data-page');
//         const pageTurn = document.getElementById(pageTurnId);

//         if(pageTurn.classList.contains('turn')) {
//             pageTurn.classList.remove('turn');
//             setTimeout(() => {
//                 pageTurn.style.zIndex = 20 - index;
//             }, 500)
//         }

//         else {
//             pageTurn.classList.add('turn');
//             setTimeout(() => {
//                 pageTurn.style.zIndex = 20 + index;
//             }, 500);
//         }
//     }
// })

// const pages = document.querySelectorAll('.book-page.page-right');
// const contactmebtn = document.querySelector('.btncontact-me');

// contactmebtn.onclick = () => {
//     pages.forEach((page, index) => {
//         setTimeout(() => {
//             page.classList.add('turn');

//             setTimeout(() => {
//                 page.style.zIndex = 20 + index;
//             }, 500)
//         }, (index + 1) * 200 + 100)
//     })
// }

// let totalPages = pages.length;
// let pageNumber = 0;

// function reverseIndex() {
//     pageNumber--;
//     if (pageNumber < 0) {
//         pageNumber = totalPages = 1;
//     }
// }

// const backprofilebutton = document.querySelector('.back-profile');

// backprofilebutton.onclick = () => {
//     pages.forEach((_, index) => {
//         setTimeout(() => {
//             reverseIndex();
//             pages[pageNumber].classList.remove('turn');

//             setTimeout(() => {
//                 reverseIndex();
//                 pages[pageNumber].style.zIndex = 10 + index;
//             }, 500)
//         }, (index + 1) * 200 + 100)
//     })
// }

// const coverRight = document.querySelector('.cover.cover-right');
// const pageLeft = document.querySelector('.book-page.page-left');

// setTimeout(() => {
//     coverRight.classList.add('turn');
// }, 2100)

// setTimeout(() => {
//     coverRight.style.zIndex = -1;
// }, 2800)

// setTimeout(() => {
//     pageLeft.style.zIndex = 20;
// }, 3200)

// pages.forEach((_, index) => {
//     setTimeout(() => {
//         reverseIndex();
//         pages[pageNumber].classList.remove('turn');

//         setTimeout(() => {
//             reverseIndex();
//             pages[pageNumber].style.zIndex = 10 + index;
//         }, 500)
//     }, (index + 1) * 200 + 2100)
// }) 









// --- Select elements ---
const pageTurnBtn = document.querySelectorAll('.nextprev-btn');
const pages = document.querySelectorAll('.book-page.page-right');
const backProfileButton = document.querySelector('.back-profile');

let totalPages = pages.length; // total number of pages
let pageNumber = 0; // current front page index

// --- Next / Previous page buttons ---
pageTurnBtn.forEach((el) => {
    el.onclick = () => {
        const pageId = el.getAttribute('data-page');
        const page = document.getElementById(pageId);
        if (!page) return;

        if (page.classList.contains('turn')) {
            // turn backward
            page.classList.remove('turn');
            page.style.zIndex = 20 - pageNumber; // flipped pages behind
            pageNumber = Math.max(pageNumber - 1, 0);
        } else {
            // turn forward
            page.classList.add('turn');
            page.style.zIndex = 20 + pageNumber; // flipped pages in front
            pageNumber = Math.min(pageNumber + 1, totalPages);
        }
    };
});

// --- Back to profile button (flip all pages backward) ---
if (backProfileButton) {
    backProfileButton.onclick = () => {
        pages.forEach((page, index) => {
            setTimeout(() => {
                page.classList.remove('turn');
                page.style.zIndex = 20 - index;
                pageNumber = 0; // reset pageNumber
            }, index * 200);
        });
    };
}

// --- Initial cover animation ---
const coverRight = document.querySelector('.cover.cover-right');
const pageLeft = document.querySelector('.book-page.page-left');

setTimeout(() => {
    if (coverRight) coverRight.classList.add('turn');
}, 2100);

setTimeout(() => {
    if (coverRight) coverRight.style.zIndex = -1;
}, 2800);

setTimeout(() => {
    if (pageLeft) pageLeft.style.zIndex = 20;
}, 3200);

// --- Auto reset all pages at load ---
pages.forEach((page, index) => {
    setTimeout(() => {
        page.classList.remove('turn');
        page.style.zIndex = 20 - index;
        pageNumber = 0; // reset
    }, (index + 1) * 200 + 2100);
});
