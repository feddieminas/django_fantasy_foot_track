// Used Google Chrome

////////////////////////////////////////////////////////////////////
/* PAGINATION */ 

/*
Sample created for our tests

<div class="container">
    <div id="listingCards_inf">
        <div class="card"><h3 class="card-header">Card1</h3></div>
        <div class="card"><h3 class="card-header">Card2</h3></div>
        <div class="card"><h3 class="card-header">Card3</h3></div>
        <div class="card"><h3 class="card-header">Card4</h3></div>
        <div class="card"><h3 class="card-header">Card5</h3></div>
    </div>
    
    <div>
        <a id="btn_prev_inf" href="javascript:prevPage()"></a>
        <a id="btn_next_inf" href="javascript:nextPage()"></a>
        <p class="p-shift"><span id="page_inf">1</span></p>
        <input id="page_input_inf">
        <a id="goto_inf" href="#"></a>
    </div>
</div>
*/

const My_All_Categories_Html = function() {
    this.container = document.getElementsByClassName("container"); // link the code to the container
};

My_All_Categories_Html.prototype.load = function() {
    let container = this.container;
    
    let ListCards = $("<div>").appendTo(container); // the div with the cards list
    $(ListCards).attr('id', 'listingCards_inf');

    for(let i = 0; i < 5; i++) { // per card elements. We will just add the div card and its card header. the card header text, we assume it as the card body
        let card = $("<div>").addClass("card").appendTo(ListCards);
        let h3 = $("<h3>").addClass("card-header").html('Card' + (i+1)).appendTo(card);
    }
        
    let PagesRefs = $("<div>").appendTo(container);
    
    let aPrev = $("<a>").appendTo(PagesRefs); //previous page button
    $(aPrev).attr('id', 'btn_prev_inf');
    $(aPrev).attr("href", "javascript:prevPage()");
    $(aPrev).text();

    let aNext = $("<a>").appendTo(PagesRefs); //next page button
    $(aNext).attr('id', 'btn_next_inf'); 
    $(aNext).attr("href", "javascript:nextPage()");
    $(aNext).text();    
        
    let p = $("<p>").appendTo(PagesRefs); // Page text indication. ex. Page : 1
    let span = $("<span>").appendTo(p);
    $(span).attr('id', 'page_inf');
    $(span).text(1);
        
    let input = $("<input>").appendTo(PagesRefs);  // Goto Page Input
    $(input).attr('id', "page_input_inf");
    $(input).text();
        
    let goto_inf = $("<a>").appendTo(PagesRefs); //Goto Page click, act as the $("#goto_inf").click 
    $(goto_inf).attr('id', 'goto_inf');   
    $(goto_inf).attr("href", "#");
    $(goto_inf).text();    
        
    return container;     
};

My_All_Categories_Html.prototype.reset = function() {
    $(this.container).html("");
        
    return true;     
};

//////////////////////////////////////////////////////////////////////

/// four slashes below means for testing purposes

const PaginationJS = function() { //set pagination global vars
    this.current_page = 1;
    this.records_per_page = 2;
    this.cardHeadElementsJQ = $('.card-header');
    this.cardsLength = this.cardHeadElementsJQ.length;
    this.myPages = {};    
};

// mPgCtgryJS is the init of new PaginationJS constructor
PaginationJS.prototype.buildMyPages = function(mPgCtgryJS) { // buildMyPages()
    mPgCtgryJS.myPages = {};
    let pager=1;
    mPgCtgryJS.myPages[String("p" + pager)] = [];
    let loopCounterRecords = 0;
    console.log(mPgCtgryJS.cardHeadElementsJQ);    
    mPgCtgryJS.cardHeadElementsJQ.each(function( i ) {
        if(this.closest('.card').style.display == "") {
            if (loopCounterRecords<mPgCtgryJS.records_per_page) {
                mPgCtgryJS.myPages[String("p" + (pager))].push(i);
                loopCounterRecords++;
		    }
		        
		    if (loopCounterRecords>=mPgCtgryJS.records_per_page) {
		        pager+=1;
				mPgCtgryJS.myPages[String("p" + (pager))] = [];
				loopCounterRecords = 0;
		    }                 
        }
    });      
    
};

PaginationJS.prototype.prevPage = function(mPgCtgryJS) { // prevPage()
    if (mPgCtgryJS.current_page > 1) {
        mPgCtgryJS.current_page--;
        mPgCtgryJS.changePage(mPgCtgryJS.current_page, mPgCtgryJS);
    }

    ////
    $('#page_inf').text(mPgCtgryJS.current_page);    
    ////
}

PaginationJS.prototype.nextPage = function(mPgCtgryJS) { // nextPage()
    if (mPgCtgryJS.current_page < mPgCtgryJS.numPages(mPgCtgryJS)) {
        mPgCtgryJS.current_page++;
        mPgCtgryJS.changePage(mPgCtgryJS.current_page, mPgCtgryJS);
    }
    
    ////
    $('#page_inf').text(mPgCtgryJS.current_page); 
    ////
}

PaginationJS.prototype.numPages = function(mPgCtgryJS) { // numPages() - calc number of pages
    return Math.ceil(mPgCtgryJS.cardsLength / mPgCtgryJS.records_per_page);
}

PaginationJS.prototype.goto_inf = function(mPgCtgryJS) { // $("#goto_inf").click - user be able to switch to desired page
    ////
    $('#goto_inf').text(); 
    ////    
    
    let gotoPageVal = String(document.getElementById("page_input_inf").value);
    gotoPageVal = (gotoPageVal=="") ? "" : gotoPageVal = gotoPageVal.match(/\d+/g) || [];
    if(gotoPageVal.length) {gotoPageVal = parseInt(gotoPageVal.join(""));}
    if (!isNaN(parseInt(gotoPageVal))) {
        if (gotoPageVal > mPgCtgryJS.numPages(mPgCtgryJS)) gotoPageVal = mPgCtgryJS.numPages(mPgCtgryJS);
        mPgCtgryJS.changePage(gotoPageVal, mPgCtgryJS);
        mPgCtgryJS.current_page = gotoPageVal;
        
        ////
        $('#goto_inf').text(mPgCtgryJS.current_page); 
        $('#page_inf').text(mPgCtgryJS.current_page); 
        ////        
    }
    
}; 

PaginationJS.prototype.changePage = function(page, mPgCtgryJS) { // changePage(page) - make page
    //pagination attrs [btns,card records,current page show value]
    let btn_next = document.getElementById("btn_next_inf");
    let btn_prev = document.getElementById("btn_prev_inf");
    let listing_cards = document.getElementById("listingCards_inf");
    let page_span = $("#page_inf");
    let goto_inf = $("#goto_inf");
    
    // Validate page
    if (page < 1) page = 1;
    if (page > mPgCtgryJS.numPages(mPgCtgryJS)) page = mPgCtgryJS.numPages(mPgCtgryJS);
    
    //check if page dict value exists
    const checkPageExists = Boolean(mPgCtgryJS.myPages[String("p" + page)] != null);
    
    //populate cards per page
    listing_cards.innerHTML = "";
    if (page_span != null && goto_inf != null) {
        page_span.parent().css({'display': 'none'});
        goto_inf.parent().parent().css({'display': 'none'});
    }
        
    if (checkPageExists) {
        for (let i = 0; i < mPgCtgryJS.myPages[String("p" + String(page))].length; i++) {
            listing_cards.innerHTML += mPgCtgryJS.cardHeadElementsJQ.eq(mPgCtgryJS.myPages[String("p" + String(page))][i]).parent()[0].outerHTML;
        }            
            
        page_span.parent().css({'display': ''});
        page_span.html(page);
        
        // buttons need to hide (last page, next button be hidden - first page, prev button be hidden) or visible
        if (page == 1) {
            btn_prev.style.visibility = "hidden";
        } else {
            btn_prev.style.visibility = "visible";
        }
        
        if (page == mPgCtgryJS.numPages(mPgCtgryJS)) {
            btn_next.style.visibility = "hidden";
        } else {
            btn_next.style.visibility = "visible";
        }  
            
        goto_inf.parent().parent().css({'display': ''});
    }
};   

////////////////////////////////////////////////////////////////////
/* AJAX */ 

const Async = function() {};
Async.prototype.fetch = function (cb) {
$.ajax('/influences/ajax/save_curr_page/')
    .done(function (data) {
        cb(data);
    });
};