from os import listdir
from os.path import isfile, join
import pandas as pd


fmt = '.png'

def get_basename(f):
    return f.split('fig/')[-1].strip(fmt)


def get_token(bn, token):
    return bn.split(token)[1].split('_')[0]


def get_fields(f):
    basename = get_basename(f)
    Bo    = get_token(basename,'Bo')
    Re    = get_token(basename,'Re')
    Ro    = get_token(basename,'Ro')
    wf    = get_token(basename,'wf')
    Gamma = get_token(basename,'Gamma')
    eta   = get_token(basename,'eta')
    mode  = get_token(basename,'mode')
    pert  = get_token(basename,'pert')
    # Save fields in dictionary
    fields = {
        'f'     : f,
        'bn'    : basename,
        'Bo'    : Bo,
        'Re'    : Re,
        'Ro'    : Ro,
        'wf'    : wf,
        'Gamma' : Gamma,
        'eta'   : eta,
        'mode'  : mode,
        'pert'  : pert,
    }
    return fields


def get_fig_dataframe():
    figpath = 'fig/'
    columns = ['Bo', 'Re', 'Ro', 'wf', 'Gamma', 'eta', 'mode', 'pert']
    order = ['Gamma','eta','Ro','Bo','Re','wf','mode','pert']

    figs = [f for f in listdir(figpath) if isfile(join(figpath, f))]
    df = pd.DataFrame(columns=columns)

    for fig in figs:
        fields = get_fields(fig)
        Bo    = fields['Bo']
        Re    = fields['Re']
        Ro    = fields['Ro']
        wf    = fields['wf']
        Gamma = fields['Gamma']
        eta   = fields['eta']
        mode  = fields['mode']
        pert  = fields['pert']

        df = df.append({'Bo':Bo, 'Re':Re, 'Ro':Ro, 'wf':wf, 'Gamma':Gamma,
            'eta':eta, 'mode':mode, 'pert':pert}, ignore_index=True)

    df = df.sort_values(by=order)
    df.reset_index(drop=True, inplace=True)
    return df


def html_head(pageInfo):
    Gamma= pageInfo[0]
    eta  = pageInfo[1]
    Ro   = pageInfo[2]
    code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../css/reset.css">
  <link rel="stylesheet" href="../css/960_24_col.css">
  <link rel="stylesheet" href="../css/text.css">
  <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="../css/monitor.css">
  <script src="js/jquery-3.4.1.min.js"></script>
  <script src="js/navigation.js"></script>
  <title>Monitor &Gamma; = {}, &eta; = {}, &Ro; = {} </title>
</head> """.format(Gamma,eta,Ro)
    return code


def html_header(code):
    code+="""
<body>
  <div class="wrap container_24">
    <header class="clearfix">
      <h1 class="grid_14">Time Series Monitors</h1>
      <nav class="grid_10">
        <ul>
          <li><a href="https://mathpost.asu.edu/~kiko">Home</a></li>
          <li>
            <button class="dropbtn" id="MenuDropBtn"
              onclick="activateMenuDropdown(this)">Results
              <i class="fa fa-caret-down"></i>
          </li>
          <li><a href="../jobs.html" target="_blank">Jobs</a></li>
        </ul>
      </nav>
    </header>
    """
    return code

def html_menu(code,fig_pages,mov_pages):
    code += """<div class="menu clearfix" id="MegaMenu">
      <div class="header">
        <h1>Knife Edge Viscosimeter</h1>
      </div>
      <div class="grid_8 alpha">
        <h3>Monitors</h3>
        <ul>"""
    for page in fig_pages:
        Gamma = page[0]
        eta   = page[1]
        Ro    = page[2]
        code+="""
          <li><a href="monitor_Gamma{}_eta{}_Ro{}.html">&Gamma; = {}, &eta; = {}, Ro = {}</a></li>""".format(
          Gamma,eta,Ro,Gamma,eta,Ro)
    code+="""
        </ul>
      </div>
      <div class="grid_8">
        <h3>Videos</h3>
        <ul>"""
    for page in mov_pages:
        Gamma = page[0]
        eta   = page[1]
        Ro    = page[2]
        code+="""
          <li><a href="monitor_Gamma{}_eta{}_Ro{}.html">&Gamma; = {}, &eta; = {}, Ro = {}</a></li>""".format(
          Gamma,eta,Ro,Gamma,eta,Ro)
    code+="""
        </ul>
      </div>
      <div class="grid_8 omega">
        <h3>Other</h3>
        <ul>
        </ul>
      </div>
    </div>"""
    return code


def html_sideNav0(code,filt_df):
    def getValue(token,str):
        return str.strip('.png').split(token)[-1].split('_')[0]

    def writeDropdownBtn(Bo):
        if float(Bo) == 0:
            Bo = '&infin;'
        code = """
      <button class="dropdown-btn" id="Bo{}"
        onclick="activateDropdown(this)">Bo = {}
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown-container">""".format(Bo,Bo)
        return code

    def writeDropdownContent(Bo,Re):
        if float(Bo) == 0:
            Bo = '&infin;'
        code = """
            <a href="#Bo{}_Re{}">Re = {}</a>""".format(Bo,Re,Re)
        return code

    code += """
    <aside id="SideNav" class="sidenav">
      <a href="javascript:void(0)" class="closebtn" id="clsSideNavBtn" onclick="closeNav()">&times;</a>i"""

    Bo = filt_df.iloc[0]['Bo']
    Re = filt_df.iloc[0]['Re']
    code+= writeDropdownBtn(Bo)
    code+= writeDropdownContent(Bo,Re)

    for i in range(filt_df.shape[0]):
        if Bo == filt_df.iloc[i]['Bo']:
            if Re != filt_df.iloc[i]['Re']:
                Re = filt_df.iloc[i]['Re']
                code+= writeDropdownContent(Bo,Re)
        else:
            code+="""
          </div>"""
            Bo = filt_df.iloc[i]['Bo']
            Re = filt_df.iloc[i]['Re']
            code+= writeDropdownBtn(Bo)
            code+= writeDropdownContent(Bo,Re)
    code+="""
      </div>
    </aside>
   """
    return code


def html_main(code,Gamma,eta):
    code += """
    <div class="main clearfix">
      <h5 class="grid_20">Parameter &Gamma; = {}, &eta; = {}. Sorted by Bo,
      Re, &omega;.</h5>
      <div class="primary grid_24">
        <button class="bodyButton" id="toTopBtn" onclick="topFunction()" title="Go to top"><i class="fa fa-angle-double-up fa-2x"></i></button>
        <button class="bodyButton" id="opnSideNavBtn" onclick="openNav()"><i class="fa fa-search fa-lg"></i></button>
    """.format(Gamma,eta)
    return code


def build_figname(Bo,Re,Ro,wf,Gamma,eta,mode,pert):
    figname = f'Ek_Bo{Bo:s}_Re{Re:s}_Ro{Ro:s}_wf{wf:s}_Gamma{Gamma:s}_eta{eta:s}_mode{mode:s}_pert{pert:s}.png'
    return figname

def html_figures(code,filt_df):
    for i in range(filt_df.shape[0]):
        Bo   = filt_df.iloc[i]['Bo']
        Re   = filt_df.iloc[i]['Re']
        Ro   = filt_df.iloc[i]['Ro']
        wf   = filt_df.iloc[i]['wf']
        Gamma= filt_df.iloc[i]['Gamma']
        eta  = filt_df.iloc[i]['eta']
        mode = filt_df.iloc[i]['mode']
        pert = filt_df.iloc[i]['pert']

        figname = build_figname(Bo,Re,Ro,wf,Gamma,eta,mode,pert)

        if float(Bo) == 0:
            Bo = '&infin;'

        if float(Ro) == 0:
            if mode == '000' and pert == '000':
                label='<b id="Bo{}_Re{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | No Perturbation</b>'.format(Bo,
                Re,Gamma,eta,Bo,Re,Ro,wf)
            else:
                label='<b id="Bo{}_Re{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | mode = {} | pert = {}</b>'.format(Bo,
                Re,Gamma,eta,Bo,Re,Ro,wf,mode,pert)
        else:
            if mode == '000' and pert == '000':
                label='<b id="Bo{}_Re{}_wf{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | No Perturbation</b>'.format(Bo,
                Re,wf,Gamma,eta,Bo,Re,Ro,wf)
            else:
                label='<b id="Bo{}_Re{}_wf{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | mode = {} | pert = {}</b>'.format(Bo,
                Re,wf,Gamma,eta,Bo,Re,Ro,wf,mode,pert)

        code += """    <hr>
        <p>
          {}
        </p>

        <img class="grid_24"
          src="fig/{}"
          alt="urts">
        """.format(label,figname)
    return code

if __name__=='__main__':
    fig_df = get_fig_dataframe()
    Nrows = fig_df.shape[0]
    Gamma = fig_df.iloc[0]['Gamma']
    eta   = fig_df.iloc[0]['eta']
    Ro    = fig_df.iloc[0]['Ro']
    fig_pages=[]
    fig_pages.append((Gamma,eta,Ro))
    for i in range(Nrows):
        if fig_df.iloc[i]['Gamma'] != Gamma or fig_df.iloc[i]['eta'] != eta or fig_df.iloc[i]['Ro'] != Ro:
            Gamma = fig_df.iloc[i]['Gamma']
            eta   = fig_df.iloc[i]['eta']
            Ro    = fig_df.iloc[i]['Ro']
            fig_pages.append((Gamma,eta,Ro))

    mov_pages=[]
#    mov_pages.append((Gamma,Ro))
#    for i in range(Nrows):
#        if mov_df.iloc[i]['Gamma'] != Gamma or mov_df.iloc[i]['eta'] != eta or mov_df.iloc[i]['Ro'] != Ro:
#            Gamma = mov_df.iloc[i]['Gamma']
#            Ro    = mov_df.iloc[i]['Ro']
#            mov_pages.append((Gamma,Ro))

    print('')
    print('Pages:')
    print(fig_pages)
    for page in fig_pages:
        Gamma = page[0]
        eta   = page[1]
        Ro    = page[2]
        # Filter dataframe
        cond  = ( (fig_df['Gamma']==Gamma) & (fig_df['eta']==eta) & (fig_df['Ro']==Ro) )
        filt_df = fig_df.iloc[fig_df.index[cond].tolist()]
        for i in range(filt_df.shape[0]):
            Bo   = filt_df.iloc[i]['Bo']
            Re   = filt_df.iloc[i]['Re']
            Ro   = filt_df.iloc[i]['Ro']
            wf   = filt_df.iloc[i]['wf']
            mode = filt_df.iloc[i]['mode']
            pert = filt_df.iloc[i]['pert']

        pageName = f'monitor_Gamma{Gamma:s}_eta{eta:s}_Ro{Ro:s}.html'
        print('')
        print(pageName)
        html = html_head(page)
        html = html_header(html)
        html = html_menu(html,fig_pages,mov_pages)
        if float(Ro) == 0:
            html = html_sideNav0(html,filt_df)
#        else:
#            html_sideNav()
        html = html_main(html,Gamma,eta)
        html = html_figures(html,filt_df)
        with open(pageName,"w") as f:
          f.write("%s" % html)
          f.close()
