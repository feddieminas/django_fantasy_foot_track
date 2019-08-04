
////////////////////////////////////////////////////////////////////
/* PAGINATION */ 

/*
<div id="listingCards_inf" >
	 <div class=“card” >
		<h3 class=“card-header” >	 Card1</h3>              
 	</div>
	 <div class=“card” >
		<h3 class=“card-header” >	 Card2</h3>              
 	</div>
	 <div class=“card” >
		<h3 class=“card-header” >	 Card3</h3>              
 	</div>
</div>

<div>
<p>Page: <span id="page_inf">1</span></p>
<input id="page_input_inf"></input>
</div>
*/

/*
mPgCtgry = new My_All_Categories_Html;
mPgCtgry.load();
mPgCtgry.reset();
mPgCtgry.container // results in an empty div
*/

const My_All_Categories_Html = function() {
    this.container = document.getElementsByClassName("container");
};

My_All_Categories_Html.prototype.load = function() {
    let container = this.container;
    
    let ListCards = $("<div>").appendTo(container);
    $(ListCards).attr('id', 'listingCards_inf');

    for(let i = 0; i < 5; i++) {
        let card = $("<div>").addClass("card").appendTo(ListCards);
        let h3 = $("<h3>").addClass("card-header").html('Card' + (i+1)).appendTo(card);
    }
        
    let PagesRefs = $("<div>").appendTo(container);
    
    let aPrev = $("<a>").appendTo(PagesRefs); 
    $(aPrev).attr('id', 'btn_prev_inf');
    $(aPrev).attr("href", "javascript:prevPage()");
    $(aPrev).text();

    let aNext = $("<a>").appendTo(PagesRefs); 
    $(aNext).attr('id', 'btn_next_inf'); 
    $(aNext).attr("href", "javascript:nextPage()");
    $(aNext).text();    
        
    let p = $("<p>").appendTo(PagesRefs);
    let span = $("<span>").appendTo(p);
    $(span).attr('id', 'page_inf');
    $(span).text(1);
        
    let input = $("<input>").appendTo(PagesRefs);  
    $(input).attr('id', "page_input_inf");
    $(input).text();
        
    return container;     
};

My_All_Categories_Html.prototype.reset = function() {
    $(this.container).html("");
        
    return true;     
};

/*
let current_page = 1;
const records_per_page = 2;
const cardHeadElementsJQ = $('.card-header');
let cardsLength = cardHeadElementsJQ.length;
let myPages = {};

    function buildMyPages() {
        myPages = {};
        let pager=1;
        myPages[String("p" + pager)] = [];
        let loopCounterRecords = 0;
        
        cardHeadElementsJQ.each(function( i ) {
            if(this.closest('.card').style.display == "") {
                if (loopCounterRecords<records_per_page) {
                    myPages[String("p" + (pager))].push(i);
                    loopCounterRecords++;
		        }
		        
		        if (loopCounterRecords>=records_per_page) {
		            pager+=1;
				    myPages[String("p" + (pager))] = [];
				    loopCounterRecords = 0;
		        }                 
            }
         });        
    }
    
    //previous btn
    function prevPage()
    {
        if (current_page > 1) {
            current_page--;
            changePage(current_page);
        }
    }

    //next btn
    function nextPage()
    {
        if (current_page < numPages()) {
            current_page++;
            changePage(current_page);
        }
    }
    
    //calc number of pages
    function numPages()
    {
        return Math.ceil(cardsLength / records_per_page);
    }   
    
    // user be able to switch to desired page
    $("#goto_inf").click(function(e) {
        let gotoPageVal = String(document.getElementById("page_input_inf").value);
        gotoPageVal = (gotoPageVal=="") ? "" : gotoPageVal.match(/\d+/g).join("");
        if (!isNaN(parseInt(gotoPageVal))) {
            if (gotoPageVal > numPages()) gotoPageVal = numPages();
            changePage(gotoPageVal);
            current_page = gotoPageVal;
        }
    });  
    
    //build page
    function changePage(page)
    {
        //pagination attrs [btns,card records,current page show value]
        let btn_next = document.getElementById("btn_next_inf");
        let btn_prev = document.getElementById("btn_prev_inf");
        let listing_cards = document.getElementById("listingCards_inf");
        let page_span = $("#page_inf");
        let goto_inf = $("#goto_inf");
    
        // Validate page
        if (page < 1) page = 1;
        if (page > numPages()) page = numPages();
    
        //check if page dict value exists
        const checkPageExists = Boolean(myPages[String("p" + page)] != null);
    
        //populate cards per page
        listing_cards.innerHTML = "";
        if (page_span != null && goto_inf != null) {
            page_span.parent().css({'display': 'none'});
            goto_inf.parent().parent().css({'display': 'none'});
        }
        
        if (checkPageExists) {
            for (let i = 0; i < myPages[String("p" + String(page))].length; i++) {
                listing_cards.innerHTML += cardHeadElementsJQ.eq(myPages[String("p" + String(page))][i]).parent()[0].outerHTML;
            }            
            
            page_span.parent().css({'display': ''});
            page_span.html(page);
        
            // buttons need to hide (last page, next button be hidden - first page, prev button be hidden) or visible
            if (page == 1) {
                btn_prev.style.visibility = "hidden";
            } else {
                btn_prev.style.visibility = "visible";
            }
        
            if (page == numPages()) {
                btn_next.style.visibility = "hidden";
            } else {
                btn_next.style.visibility = "visible";
            }  
            
            goto_inf.parent().parent().css({'display': ''});
        }
        
    }        
*/    

////////////////////////////////////////////////////////////////////
/* AJAX */ 

const Async = function() {};
Async.prototype.fetch = function (cb) {
$.ajax('/influences/ajax/save_curr_page/')
    .done(function (data) {
        cb(data);
    });
};