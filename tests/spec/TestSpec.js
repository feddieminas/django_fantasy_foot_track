
////////////////////////////////////////////////////////////////////
/* PAGINATION */ 


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
