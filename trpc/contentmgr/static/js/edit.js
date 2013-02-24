var mkdwn, in_out, current_scroll;
mkdwn = new Markdown.Converter();

$(document).ready(function () {
    in_out = {
        'out_title' : $('#preview .content .title'),
        'out_body' : $('#preview .content .content_body'),
        'out_ext' : $('#preview .content_ext'),
        'in_title' : $('#id_title'),
        'in_body' : $('#id_body')
    };
    
    in_out['in_all'] = in_out.in_title.add(in_out.in_body);

    in_out.in_all.keydown(function () {
        update_preview();
    });
    in_out.in_all.keyup(function () {
        update_preview();
    });
    in_out.in_body.click(function () {
        update_scroll();
    });


});

function update_preview() {
    in_out.out_title[0].innerHTML = in_out.in_title.val();
    in_out.out_body[0].innerHTML = mkdwn.makeHtml(in_out.in_body.val());
    update_scroll();
}

function update_scroll() {
    var scroll_to, in_txt, sel_start, p_count, scroll_offset;
    if(!check_autoscroll()) {
        return false;
    }

    scroll_to = 0;
    
    scroll_offset = $(in_out.out_body.find('p')[0]).position().top;
    sel_start = in_out.in_body[0].selectionStart;
    in_txt = in_out.in_body.val().substr(0, sel_start);
    p_count = ("\n\n"+in_txt).match(/\n\n/g).length - 1;
    try {
        scroll_to = $(in_out.out_body.find('>*')[p_count]).position().top;
    } catch(err) {
        scroll_to = in_out.out_body.children().last().position().top;
    }
    //in_out.out_ext[0].scrollTop = scroll_to - scroll_offset;
    smooth_scroll(in_out.out_ext[0], scroll_to - scroll_offset - 20);
    return true;
}

function smooth_scroll(target, scroll_to) {
    var scroll_start, duration, px_per_tick, ms_per_frame, frames, new_top, u_bound, l_bound;
    scroll_start = target.scrollTop;
    if(scroll_to < 0) {
        scroll_to = 0;
    }

    if(scroll_start == scroll_to) {
        return false;
    }
    clearInterval(current_scroll);
    duration = 300; //duration in ms
    ms_per_frame = 50;
    frames = duration / ms_per_frame;
    px_per_tick = (scroll_to - scroll_start) / frames;

    current_scroll = setInterval(function () {
        new_top = target.scrollTop + px_per_tick;
        if(target.scrollTop < scroll_to && scroll_to <= new_top) {
            target.scrollTop = scroll_to;
            clearInterval(current_scroll);
        } else if (new_top <= scroll_to && scroll_to < target.scrollTop) {
            target.scrollTop = scroll_to;
            clearInterval(current_scroll);
        } else {
            target.scrollTop = new_top;
        }
    }, ms_per_frame);

/*    setTimeout(function () {
        clearInterval(current_scroll);
    }, duration + ms_per_frame);
*/
    return true;
}

function check_autoscroll() {
    return document.getElementById('auto_scroll').checked;
}
