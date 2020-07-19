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
    df_float = pd.DataFrame(columns=columns)

    # Get string dataFrame
    for fig in figs:
        fields = get_fields(fig)
        if fields['Bo']=='0e0':
            Bo = 'Inf'
        else:
            Bo = fields['Bo']
        Re    = fields['Re']
        Ro    = fields['Ro']
        wf    = fields['wf']
        Gamma = fields['Gamma']
        eta   = fields['eta']
        mode  = fields['mode']
        pert  = fields['pert']

        df = df.append({'Bo':Bo, 'Re':Re, 'Ro':Ro, 'wf':wf, 'Gamma':Gamma,
            'eta':eta, 'mode':mode, 'pert':pert}, ignore_index=True)

    # Get floats dataFrame
    for column in columns:
        df_float[column] = pd.to_numeric(df[column],downcast='float')

    # Sort floats dataFrame
    df_float = df_float.sort_values(by=order,ascending=False)

    # Sort string dataFrame using floats dataFrame
    aux = df
    df = aux.iloc[df_float.index[range(df_float.index.shape[0])]]
    df.reset_index(drop=True,inplace=True)

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
      <h1 class="grid_14">Time Series - 3D Axisymmetric</h1>
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
        if Bo == 'Inf':
            Bo = '&infin;'
        code = """
      <button class="dropdown-btn" id="Bo{}"
        onclick="activateDropdown(this)">Bo = {}
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown-container">""".format(Bo,Bo)
        return code

    def writeDropdownContent(Bo,Re):
        if Bo == 'Inf':
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
      <h5 class="grid_20">Parameters &Gamma; = {}, &eta; = {}.<br> Sorted by Bo,
      Re, &omega;.</h5>
      <div class="primary grid_24">
        <button class="bodyButton" id="toTopBtn" onclick="topFunction()" title="Go to top"><i class="fa fa-angle-double-up fa-2x"></i></button>
        <button class="bodyButton" id="opnSideNavBtn" onclick="openNav()"><i class="fa fa-search fa-lg"></i></button>
    """.format(Gamma,eta)
    return code


def build_figname(Bo,Re,Ro,wf,Gamma,eta,mode,pert):
    if Bo == 'Inf':
        Bo = '0e0'
    figname = f'Ek_Bo{Bo:s}_Re{Re:s}_Ro{Ro:s}_wf{wf:s}_Gamma{Gamma:s}_eta{eta:s}_mode{mode:s}_pert{pert:s}.png'
    return figname

def format_number(N):
    N_format = int(float(N)) if float(N).is_integer() else float(N)
    return str(N_format)

def html_figures(code,filt_df):
    for i in range(filt_df.shape[0]):
        Bo_id   = filt_df.iloc[i]['Bo']
        Re_id   = filt_df.iloc[i]['Re']
        Ro_id   = filt_df.iloc[i]['Ro']
        wf_id   = filt_df.iloc[i]['wf']
        Gamma_id= filt_df.iloc[i]['Gamma']
        eta_id  = filt_df.iloc[i]['eta']
        mode_id = filt_df.iloc[i]['mode']
        pert_id = filt_df.iloc[i]['pert']

        Bo   = format_number(Bo_id)
        Re   = format_number(Re_id)
        Ro   = format_number(Ro_id)
        wf   = format_number(wf_id)
        Gamma= format_number(Gamma_id)
        eta  = format_number(eta_id)
        mode = format_number(mode_id)
        pert = format_number(pert_id)

        figname = build_figname(Bo_id,Re_id,Ro_id,wf_id,
                Gamma_id,eta_id,mode_id,pert_id)

        if Bo_id == 'Inf':
            Bo    = '&infin;'
            Bo_id = '&infin;'

        if float(Ro) == 0:
            if mode == '000' and pert == '000':
                label='<b id="Bo{}_Re{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | No Perturbation</b>'.format(Bo_id,
                Re_id,Gamma,eta,Bo,Re,Ro,wf)
            else:
                label='<b id="Bo{}_Re{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | mode = {} | pert = {}</b>'.format(Bo_id,
                Re_id,Gamma,eta,Bo,Re,Ro,wf,mode,pert)
        else:
            if mode == '000' and pert == '000':
                label='<b id="Bo{}_Re{}_wf{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | No Perturbation</b>'.format(Bo_id,
                Re_id,wf_id,Gamma,eta,Bo,Re,Ro,wf)
            else:
                label='<b id="Bo{}_Re{}_wf{}">&Gamma; = {} | &eta; = {} | Bo = {} | Re = {} | \
Ro = {} | &omega;<sub>f</sub> = {} | mode = {} | pert = {}</b>'.format(Bo_id,
                Re_id,wf_id,Gamma,eta,Bo,Re,Ro,wf,mode,pert)

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
    df = get_fig_dataframe()
    Nrows = df.shape[0]
    Gamma = df.iloc[0]['Gamma']
    eta   = df.iloc[0]['eta']
    Ro    = df.iloc[0]['Ro']
    fig_pages = []
    fig_pages.append((Gamma,eta,Ro))
    for i in range(Nrows):
        if df.iloc[i]['Gamma'] != Gamma or df.iloc[i]['eta'] != eta or df.iloc[i]['Ro'] != Ro:
            Gamma = df.iloc[i]['Gamma']
            eta   = df.iloc[i]['eta']
            Ro    = df.iloc[i]['Ro']
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
        cond  = ( (df['Gamma']==Gamma) & (df['eta']==eta) & (df['Ro']==Ro) )
        filt_df = df.iloc[df.index[cond].tolist()]
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
        html = html_main(html,format_number(Gamma),format_number(eta))
        html = html_figures(html,filt_df)
        with open(pageName,"w") as f:
          f.write("%s" % html)
          f.close()
