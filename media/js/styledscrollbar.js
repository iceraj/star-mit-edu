var StyledScrollbar = new Class({
    Extends: Slider,

    Implements: [Events, Options],

    Binds: ['resizeScrollbar', 'onMouseLeave'],
    
    initialize: function(content,scrollbar,handle,options){
        this.setOptions(options);
        this.content = document.id(content);
        this.scrollbar = document.id(scrollbar);
        this.handle = document.id(handle);
        this.ignoreMouse = this.options.ignoreMouse;
        this.horizontal = this.options.horizontal;

        // handle window resizing
        this.options.steps = (this.horizontal?(content.getScrollSize().x - content.getSize().x):(content.getScrollSize().y - content.getSize().y))

        // hide slider if there's enough room to display all content
        if (parseInt(this.options.steps) == 0) {
            scrollbar.setStyle('display', 'none');
        }

        // add listener for slider change events
        this.addEvent('onChange', this.onChange);

        // add window resize handler to properly resize/reconfig slider
        window.onresize = this.resizeScrollbar;

        if( !(this.ignoreMouse) ){
            // Scroll the content element when the mousewheel is used within the 
            // content or the scrollbar element.
            $$(this.content, this.scrollbar).addEvent('mousewheel', function(e){  
                e = new Event(e).stop();
                var step = this.step - e.wheel * 30;  
                this.set(step);                   
            }.bind(this));
        }

        // call super
        this.parent(scrollbar, handle, options);

        // Stops the handle dragging process when the mouse leaves the document body.
        //$(document.body).addEvent('mouseleave',this.onMouseLeave);

        // set scrollbar to 0
        this.set(0);
        this.resizeScrollbar();
    },

    onMouseLeave: function() {
        this.drag.stop();
    },

    onChange: function(step) {
        // Scrolls the content element in x or y direction.
        var x = (this.horizontal?step:0);
        var y = (this.horizontal?0:step);
        this.content.scrollTo(x,y);
    },

    resizeScrollbar: function() {
        this.options.steps = (this.horizontal?(this.content.getScrollSize().x - this.content.getSize().x):(this.content.getScrollSize().y - this.content.getSize().y));
        //this.handle.setStyle('width', this.content.getScrollSize().x*this.content.getScrollSize().x/this.content.getSize() + '%');
        if (parseInt(this.options.steps) == 0) {
            this.scrollbar.setStyle('display', 'none');
            this.content.scrollTo(0,0);
        } else {
        var offset;
            this.scrollbar.setStyle('display', 'block');
        }
        switch (this.options.mode){
            case 'vertical':
                this.axis = 'y';
                this.property = 'top';
                offset = 'offsetHeight';
                break;
            case 'horizontal':
                this.axis = 'x';
                this.property = 'left';
                offset = 'offsetWidth';
                break;
        }
        this.half = this.knob[offset] / 2;
        this.full = this.element[offset] - this.knob[offset] + (this.options.offset * 2);
        this.min =  0;
        this.max = this.options.steps;
        this.range = this.max - this.min;
        this.steps = this.options.steps || this.full;
        this.stepSize = Math.abs(this.range) / this.steps;
        this.stepWidth = this.stepSize * this.full / Math.abs(this.range) ;
        //this.knob.setStyle('position', 'relative').setStyle(this.property, - this.options.offset); // this killed konqueror
        this.drag.options.limit[this.axis] = [- this.options.offset, this.full - this.options.offset];
    }
});

window.addEvent('domready', function(){            
    new StyledScrollbar( $('scroller_wrapper'), $('scrollbar'), $('handle'), {
        horizontal: true
    });
});
