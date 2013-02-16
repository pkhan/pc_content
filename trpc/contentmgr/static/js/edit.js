var mkdwn, in_out;
mkdwn = new Markdown.Converter();

$(document).ready(function () {
    in_out = {
        'out_title' : $('#preview .content .title'),
        'out_body' : $('#preview .content .content_body'),
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


});

function update_preview() {
    in_out.out_title[0].innerHTML = in_out.in_title.val();
    in_out.out_body[0].innerHTML = mkdwn.makeHtml(in_out.in_body.val());
}
