
////////////////////////////////////////////////////////////////////
/* PAGINATION */ 

describe("Pagination html and js", function() {
    beforeEach(function() {
        mPgCtgry = new My_All_Categories_Html;
        mPgCtgry.load();
        
        mPgCtgryJS = new PaginationJS;        
    });
    
    afterEach(function() {
        mPgCtgry.reset();
    });    

    it("some init variables on html", function() {
        expect(parseInt($('#page_inf').text())).toEqual(1); //Current Page : 1
        expect($('.card').find('.card-header').text().slice(0,5)).toEqual('Card1'); // first card
        expect($('.card').find('.card-header').text().slice(-5,-1) +$('.card').find('.card-header').text().slice(-1)).toEqual('Card5'); //last card
    });
    
    describe("Page Dict function", function() {
        it("should return per page numbers equal to records_per_page set", function() {
            mPgCtgryJS.buildMyPages(mPgCtgryJS);
            expect(mPgCtgryJS.myPages["p1"].length).toEqual(mPgCtgryJS.records_per_page); // verify records per page -- 5 cards in total, we have set 2 records thus 2
            expect(mPgCtgryJS.myPages["p3"].length + mPgCtgryJS.myPages["p3"][0]).toEqual(5); // sum of last page length 1 plus last card index [4] -- 5 cards in total, we have set 2 records thus 1 last card on last page
            expect(Object.keys(mPgCtgryJS.myPages).length).toEqual(mPgCtgryJS.numPages(mPgCtgryJS)); // verify number of pages in page dict is equal to the calc of numpages() function - 3 equals to 3
        });
    });
    
    describe("Next - Prev Page and div list container", function() {
        it("should return next page 2 and then prev page is 1 and cards accordingly", function() {
          mPgCtgryJS.buildMyPages(mPgCtgryJS); //create the page dict to loop cards per page accordingly
          mPgCtgryJS.nextPage(mPgCtgryJS); // retrieve next page cards
          expect(mPgCtgryJS.current_page).toEqual(2); // Current Page : 1 thus next page is 2
          expect(mPgCtgryJS.myPages["p2"]).toEqual(jasmine.objectContaining([2,3])); // cards indices are [0,1,2,3,4], thus of second page of two records will be [2,3] 
          expect($('#listingCards_inf .card').length).toEqual(2); // verify that cards printed in html are two
          mPgCtgryJS.prevPage(mPgCtgryJS); // retrieve previous page cards 
          expect(mPgCtgryJS.current_page).toEqual(1); // Current Page : 2 thus prev page is 1
          expect(mPgCtgryJS.myPages["p1"]).toEqual(jasmine.objectContaining([0,1])); // cards indices are [0,1,2,3,4], thus of first page of two records will be [0,1] 
          expect($('#listingCards_inf .card').length).toEqual(2); // verify that cards printed in html are two
          expect(document.getElementById("btn_prev_inf").style.visibility).toEqual("hidden"); // on Page 1 : no prev button
        });
    });    
    
    describe("goto_inf function", function() {
        it("should test input numbers and/or text action - go to the right page and retrieve correct card(s)", function() {
          $('#page_input_inf').val(); // insert an empty text
          mPgCtgryJS.buildMyPages(mPgCtgryJS);
          mPgCtgryJS.goto_inf(mPgCtgryJS);
          expect($('#goto_inf').text()).toEqual('');
          $('#page_input_inf').val('bfbfkf'); // insert a text
          mPgCtgryJS.buildMyPages(mPgCtgryJS);
          mPgCtgryJS.goto_inf(mPgCtgryJS);
          expect($('#goto_inf').text()).toEqual('');  
          $('#page_input_inf').val('3fbfbif4'); ////insert mix of text and numbers - assure it goes to max page 3
          mPgCtgryJS.buildMyPages(mPgCtgryJS);
          mPgCtgryJS.goto_inf(mPgCtgryJS);
          expect(parseInt($('#goto_inf').text())).toEqual(mPgCtgryJS.current_page);  
          $('#page_input_inf').val(3); //insert a number
          mPgCtgryJS.buildMyPages(mPgCtgryJS);
          mPgCtgryJS.goto_inf(mPgCtgryJS);
          expect(parseInt($('#goto_inf').text())).toEqual(mPgCtgryJS.current_page);            
          expect($('.card').find('.card-header').text().slice(0,5)).toEqual('Card5'); // fifth last card found on last page
          expect(document.getElementById("btn_next_inf").style.visibility).toEqual("hidden"); // on Page 3 last : no next button
         });
    });    
    
});

/////////////////////////////////////////////////////////////////////////
/* AJAX */ 

//Ajax for all categories html - test One
describe("Async", function () {
    it("should fetch from a server", function () {
        var async = new Async();

        // creating our spied callback
        var callback = jasmine.createSpy('callback');
        var data = [
              {'got_saved': true},
        ];

        spyOn($, 'ajax').and.callFake(function (req) {
            var d = $.Deferred();
           // resolve using our mock data
            d.resolve(data);
            return d.promise();
        });

        async.fetch(callback);

        // grabbing the returned arguments from the spied call:
        var fakeData = callback.calls.mostRecent().args[0];
        expect(fakeData[0].got_saved).toEqual(data[0].got_saved);
    });
}); 

//Ajax for all categories html - test two
describe("mocking ajax", function() {

  describe("suite wide usage", function() {

    beforeEach(function() {
      jasmine.Ajax.install();
    });

    afterEach(function() {
      jasmine.Ajax.uninstall();
    });

    it("specifying response when you need it", function() {
      var doneFn = jasmine.createSpy("success");

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function(args) {
        if (this.readyState == this.DONE) {
          doneFn(this.responseText);
        }
      };

      xhr.open("GET", "/influences/ajax/save_curr_page/");
      xhr.send();

      expect(jasmine.Ajax.requests.mostRecent().url).toBe('/influences/ajax/save_curr_page/');
      expect(doneFn).not.toHaveBeenCalled();

      jasmine.Ajax.requests.mostRecent().respondWith({

        "status": 200,

        "contentType": 'application/json',

        "responseText": JSON.stringify({'got_saved': true})
      });

      expect(doneFn).toHaveBeenCalledWith(JSON.stringify({'got_saved': true}));
    });


  });

});
