function toggletab(tabnum)
{
    document.getElementsByClassName('active-tab')[0].classList.toggle('active-tab');
    document.getElementsByClassName('link-tab')[tabnum].classList.toggle('active-tab');

    var t0 = document.getElementById('tab-home');
    var t1 = document.getElementById('tab-results');

    switch(tabnum)
    {
        case 0:
            t0.style.left = '0vw';
            t1.style.left = '-100vw';
            if(window.matchMedia("(min-width: 800px)").matches)
            {
                t0.style.width = 'calc(100vw - 20rem)';
                t1.style.width = 'calc(100vw - 20rem)';
                t1.style.left = 'calc(-100vw + 20rem)';
            }
        break;
        case 1:
            t0.style.left = '-100vw';
            t1.style.left = '0vw';
            if(window.matchMedia("(min-width: 800px)").matches)
            {
                t0.style.width = 'calc(100vw - 20rem)';
                t1.style.width = 'calc(100vw - 20rem)';
                t0.style.left = 'calc(-100vw + 20rem)';
            }
            document.getElementById('search-results').focus();
        break;
        default: break;
    }
}

function togglepoints(x)
{
    var cont = document.getElementById('points-container');
    switch(x)
    {
        case 0:
            cont.style.top = "-100vh";
        break;
        case 1:
            cont.style.top = "0vh";
        break;
    }
}

function searchresults(inp)
{
    var key = inp.value.toLowerCase();
    console.log(key);
    var result_list = document.getElementsByClassName('result');

    for(var i = 0; i < result_list.length; i++)
    {
        var title = result_list[i].childNodes[1];
        if(title.textContent.toLowerCase().indexOf(key) == -1)
        {
            var listitems = title.nextElementSibling.childNodes;
            var flag = 0;
            for(var j=0; j<listitems.length; j++)
            {
                if(listitems[j].nodeType != 1) continue;
                if(listitems[j].textContent.toLowerCase().indexOf(key) == -1) flag++;
            }
            if(flag == 3) result_list[i].style.display = 'none';
            else result_list[i].style.display = 'block';
        }
        else result_list[i].style.display = 'block';
    }
}
